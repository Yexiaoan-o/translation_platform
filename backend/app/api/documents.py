from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import os
from app.services.document_service import DocumentService

router = APIRouter()
document_service = DocumentService()

@router.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    """
    解析文档，提取文本内容
    """
    try:
        content = await document_service.parse_document(file)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/export/{project_id}")
async def export_document(project_id: int, format: str = "markdown"):
    """
    导出翻译后的文档
    """
    try:
        file_path = await document_service.export_document(project_id, format)
        return FileResponse(
            path=file_path,
            filename=f"translated_document.{format}",
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))