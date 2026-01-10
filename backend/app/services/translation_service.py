from typing import List
from app.schemas.translation import TranslationRequest, TranslationResponse, SegmentResponse
import markdown

class TranslationService:
    def __init__(self):
        # 这里可以初始化翻译记忆库和术语库连接
        self.segments = []
        self.segment_id_counter = 1

    async def translate(self, text: str, source_language: str, target_language: str):
        # 模拟翻译功能
        # 实际项目中这里可以集成机器翻译API
        translated_text = f"[Translated] {text}"
        return TranslationResponse(
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language
        )

    async def get_segments(self, project_id: int):
        # 模拟获取项目的翻译段落
        project_segments = []
        for segment in self.segments:
            if segment["project_id"] == project_id:
                project_segments.append(SegmentResponse(**segment))
        
        if not project_segments:
            # 如果没有段落，创建一些模拟数据
            mock_segments = [
                {
                    "id": self.segment_id_counter,
                    "project_id": project_id,
                    "source_text": "Hello, how are you?",
                    "target_text": "",
                    "status": "untranslated"
                },
                {
                    "id": self.segment_id_counter + 1,
                    "project_id": project_id,
                    "source_text": "I am fine, thank you.",
                    "target_text": "",
                    "status": "untranslated"
                }
            ]
            self.segment_id_counter += 2
            self.segments.extend(mock_segments)
            project_segments = [SegmentResponse(**segment) for segment in mock_segments]
        
        return project_segments

    async def update_segment(self, segment_id: int, target_text: str, status: str):
        # 模拟更新翻译段落
        for segment in self.segments:
            if segment["id"] == segment_id:
                segment["target_text"] = target_text
                segment["status"] = status
                return
        raise Exception(f"Segment with id {segment_id} not found")