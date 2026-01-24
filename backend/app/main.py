import os, uuid, logging
from fastapi import FastAPI, UploadFile, File, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.engine.parsers.markdown import MarkdownEngine
from app.db.ddb_client import DDBManager
from app.engine.llm import LLMTranslator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

engine = MarkdownEngine()
db_manager = DDBManager()
translator = LLMTranslator()
UPLOAD_DIR = "data/originals"

class SaveRequest(BaseModel):
    seg_id: int
    target: str

@app.post("/api/v1/parse")
async def parse_md(file: UploadFile = File(...), use_mt: str = Query("false")):
    content = (await file.read()).decode("utf-8")
    project_id = str(uuid.uuid4())
    # 存原文
    if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)
    with open(os.path.join(UPLOAD_DIR, f"{project_id}.md"), "w", encoding="utf-8") as f: f.write(content)
    
    segments = engine.parse_to_segments(content)
    if use_mt.lower() == "true":
        segments = await translator.translate_segments_concurrency(segments)
    
    db_manager.save_project(project_id, file.filename, segments)
    return {"project_id": project_id, "segments": segments}

@app.get("/api/v1/projects")
async def list_projects(): return db_manager.get_all_projects()

@app.get("/api/v1/project/{project_id}")
async def get_project(project_id: str): return {"segments": db_manager.load_segments(project_id)}

@app.post("/api/v1/project/{project_id}/save")
async def save(project_id: str, req: SaveRequest):
    db_manager.update_segment_translation(project_id, req.seg_id, req.target)
    return {"status": "ok"}

@app.post("/api/v1/export/{project_id}")
async def export(project_id: str, translations: dict = Body(...)):
    with open(os.path.join(UPLOAD_DIR, f"{project_id}.md"), "r", encoding="utf-8") as f: original = f.read()
    return {"markdown": engine.render_translation(original, translations)}

@app.delete("/api/v1/project/{project_id}")
async def delete_project(project_id: str):
    try:
        # 1. 从数据库中删除
        db_manager.delete_project(project_id)
        
        # 2. (可选) 删除磁盘上的原文备份
        file_path = os.path.join(UPLOAD_DIR, f"{project_id}.md")
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {"status": "success", "message": f"Project {project_id} deleted"}
    except Exception as e:
        logger.error(f"删除失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))