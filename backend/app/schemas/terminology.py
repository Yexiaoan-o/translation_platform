from pydantic import BaseModel
from typing import Optional

class TermBase(BaseModel):
    source_term: str
    target_term: str
    source_language: str
    target_language: str
    domain: Optional[str] = None
    definition: Optional[str] = None

class TermCreate(TermBase):
    pass

class TermList(BaseModel):
    id: int
    source_term: str
    target_term: str
    source_language: str
    target_language: str
    domain: Optional[str] = None

    class Config:
        from_attributes = True

class TermResponse(TermBase):
    id: int

    class Config:
        from_attributes = True