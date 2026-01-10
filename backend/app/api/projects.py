from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectList
from app.services.project_service import ProjectService

router = APIRouter()
project_service = ProjectService()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    name: str = Form(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
    files: List[UploadFile] = File(...)
):
    """
    创建新项目并上传文件
    """
    try:
        project = await project_service.create_project(
            name=name,
            source_language=source_language,
            target_language=target_language,
            files=files
        )
        return project
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProjectList])
async def get_projects():
    """
    获取所有项目列表
    """
    try:
        projects = await project_service.get_projects()
        return projects
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """
    获取项目详情
    """
    try:
        project = await project_service.get_project(project_id)
        return project
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """
    删除项目
    """
    try:
        await project_service.delete_project(project_id)
        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))