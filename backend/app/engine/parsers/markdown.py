import re

class MarkdownEngine:
    def parse_to_segments(self, text: str):
        # 简单实现：按行分割并过滤空行，保留 ID
        lines = text.split('\n')
        segments = []
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'): # 简单过滤掉标题或空行
                segments.append({"id": i, "source": line.strip(), "target": ""})
        return segments

    def render_translation(self, original_text: str, translations: dict):
        lines = original_text.split('\n')
        result = []
        for i, line in enumerate(lines):
            # 这里的 str(i) 是因为前端传回的 JSON key 通常是字符串
            if str(i) in translations:
                result.append(translations[str(i)])
            else:
                result.append(line)
        return '\n'.join(result)