from typing import List
from app.schemas.translation import TranslationRequest, TranslationResponse, SegmentResponse
import markdown

class TranslationService:
    def __init__(self, project_service):
        # 这里可以初始化翻译记忆库和术语库连接
        self.segments = []
        self.segment_id_counter = 1
        self.project_service = project_service

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
        # 检查是否已有段落
        project_segments = []
        for segment in self.segments:
            if segment["project_id"] == project_id:
                project_segments.append(SegmentResponse(**segment))
        
        if not project_segments:
            # 从项目文件中提取段落
            project_segments = await self.extract_segments_from_files(project_id)
        
        return project_segments

    async def extract_segments_from_files(self, project_id: int):
        # 从项目文件中提取翻译段落
        project_files = await self.project_service.get_project_files(project_id)
        segments = []
        
        for file in project_files:
            filename = file["filename"]
            content = file["content"]
            
            if filename.endswith('.md'):
                # 处理Markdown文件
                segments.extend(self._extract_segments_from_markdown(content, project_id))
            elif filename.endswith('.txt'):
                # 处理文本文件
                segments.extend(self._extract_segments_from_text(content, project_id))
            else:
                # 处理其他文件类型（简化处理）
                segments.append({
                    "id": self.segment_id_counter,
                    "project_id": project_id,
                    "source_text": f"[File: {filename}]\n{content[:500]}...",
                    "target_text": "",
                    "status": "untranslated"
                })
                self.segment_id_counter += 1
        
        if not segments:
            # 如果没有提取到段落，创建一些模拟数据
            segments = [
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
        
        # 保存段落
        self.segments.extend(segments)
        
        return [SegmentResponse(**segment) for segment in segments]

    def _extract_segments_from_markdown(self, content: str, project_id: int):
        # 从Markdown文件中提取句子
        segments = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 处理标题行
            if line.startswith('#'):
                # 标题作为单独的段落
                segments.append({
                    "id": self.segment_id_counter,
                    "project_id": project_id,
                    "source_text": line,
                    "target_text": "",
                    "status": "untranslated"
                })
                self.segment_id_counter += 1
            else:
                # 处理正文行，以句子为单位分割
                sentences = self._split_into_sentences(line)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 5:  # 忽略太短的句子
                        segments.append({
                            "id": self.segment_id_counter,
                            "project_id": project_id,
                            "source_text": sentence,
                            "target_text": "",
                            "status": "untranslated"
                        })
                        self.segment_id_counter += 1
        
        return segments

    def _extract_segments_from_text(self, content: str, project_id: int):
        # 从文本文件中提取句子
        segments = []
        
        # 以句子为单位分割
        sentences = self._split_into_sentences(content)
        
        # 创建句子级别的段落
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 5:  # 忽略太短的句子
                segments.append({
                    "id": self.segment_id_counter,
                    "project_id": project_id,
                    "source_text": sentence,
                    "target_text": "",
                    "status": "untranslated"
                })
                self.segment_id_counter += 1
        
        return segments

    def _split_into_sentences(self, text: str):
        # 将文本分割为句子
        import re
        
        # 处理空文本
        if not text:
            return []
        
        # 使用正则表达式分割句子，支持中英文标点
        # 改进的正则表达式，支持更多句子结束符和空格情况
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\。|\？|\！)(?=\s|$)'
        sentences = re.split(sentence_pattern, text)
        
        # 清理和过滤句子
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                cleaned_sentences.append(sentence)
        
        # 处理边界情况
        if not cleaned_sentences:
            return [text]
        
        return cleaned_sentences

    async def update_segment(self, segment_id: int, target_text: str, status: str):
        # 模拟更新翻译段落
        for segment in self.segments:
            if segment["id"] == segment_id:
                segment["target_text"] = target_text
                segment["status"] = status
                return
        raise Exception(f"Segment with id {segment_id} not found")