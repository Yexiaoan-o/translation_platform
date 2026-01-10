from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.translation import TranslationRequest, TranslationResponse, SegmentResponse
from app.services.translation_service import TranslationService
from app.api.projects import project_service

router = APIRouter()
translation_service = TranslationService(project_service)

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    翻译文本
    """
    try:
        result = await translation_service.translate(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/segments/{project_id}", response_model=List[SegmentResponse])
async def get_segments(project_id: int):
    """
    获取项目的所有翻译段落
    """
    try:
        segments = await translation_service.get_segments(project_id)
        return segments
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/segments/{segment_id}")
async def update_segment(segment_id: int, target_text: str, status: str):
    """
    更新翻译段落
    """
    try:
        await translation_service.update_segment(
            segment_id=segment_id,
            target_text=target_text,
            status=status
        )
        return {"message": "Segment updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))