from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.terminology import TermCreate, TermResponse, TermList
from app.services.terminology_service import TerminologyService

router = APIRouter()
terminology_service = TerminologyService()

@router.post("/", response_model=TermResponse)
async def create_term(term: TermCreate):
    """
    创建新术语
    """
    try:
        result = await terminology_service.create_term(term)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TermList])
async def get_terms(
    source_language: str = None,
    target_language: str = None,
    domain: str = None
):
    """
    获取术语列表，支持筛选
    """
    try:
        terms = await terminology_service.get_terms(
            source_language=source_language,
            target_language=target_language,
            domain=domain
        )
        return terms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{term_id}", response_model=TermResponse)
async def get_term(term_id: int):
    """
    获取术语详情
    """
    try:
        term = await terminology_service.get_term(term_id)
        return term
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{term_id}", response_model=TermResponse)
async def update_term(term_id: int, term: TermCreate):
    """
    更新术语
    """
    try:
        result = await terminology_service.update_term(term_id, term)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{term_id}")
async def delete_term(term_id: int):
    """
    删除术语
    """
    try:
        await terminology_service.delete_term(term_id)
        return {"message": "Term deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))