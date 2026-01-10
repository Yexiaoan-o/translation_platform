from typing import List, Optional
from datetime import datetime
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectList
import os

class ProjectService:
    def __init__(self):
        # 这里可以初始化数据库连接等
        self.projects = []
        self.project_id_counter = 1
        self.file_contents = {}  # 存储文件内容，按项目ID组织

    async def create_project(self, name: str, source_language: str, target_language: str, files: List):
        # 模拟创建项目
        project = {
            "id": self.project_id_counter,
            "name": name,
            "source_language": source_language,
            "target_language": target_language,
            "created_at": datetime.now(),
            "files": [file.filename for file in files]
        }
        self.project_id_counter += 1
        self.projects.append(project)
        
        # 保存文件内容
        project_files = []
        for file in files:
            file_content = await file.read()
            project_files.append({
                "filename": file.filename,
                "content": file_content.decode('utf-8') if isinstance(file_content, bytes) else file_content
            })
        self.file_contents[project["id"]] = project_files
        
        return ProjectResponse(**project)

    async def get_projects(self):
        # 模拟获取项目列表
        return [
            ProjectList(
                id=project["id"],
                name=project["name"],
                source_language=project["source_language"],
                target_language=project["target_language"],
                created_at=project["created_at"]
            )
            for project in self.projects
        ]

    async def get_project(self, project_id: int):
        # 模拟获取项目详情
        for project in self.projects:
            if project["id"] == project_id:
                return ProjectResponse(**project)
        raise Exception(f"Project with id {project_id} not found")

    async def delete_project(self, project_id: int):
        # 模拟删除项目
        for i, project in enumerate(self.projects):
            if project["id"] == project_id:
                self.projects.pop(i)
                if project_id in self.file_contents:
                    del self.file_contents[project_id]
                return
        raise Exception(f"Project with id {project_id} not found")

    async def get_project_files(self, project_id: int):
        # 获取项目的文件内容
        if project_id not in self.file_contents:
            return []
        return self.file_contents[project_id]