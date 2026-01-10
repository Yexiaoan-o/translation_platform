from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    source_language: str
    target_language: str

class ProjectCreate(ProjectBase):
    pass

class ProjectList(BaseModel):
    id: int
    name: str
    source_language: str
    target_language: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    files: List[str]

    class Config:
        from_attributes = True