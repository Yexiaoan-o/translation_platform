from pydantic import BaseModel
from typing import Optional

class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str

class SegmentBase(BaseModel):
    source_text: str
    target_text: Optional[str] = None
    status: str = "untranslated"

class SegmentCreate(SegmentBase):
    project_id: int

class SegmentResponse(SegmentBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True