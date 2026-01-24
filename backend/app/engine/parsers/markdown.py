import re

class MarkdownEngine:
    def __init__(self):
        # 识别不需要翻译的结构
        self.ignore_pattern = re.compile(r'^(\s*```.*|\s*---+\s*|\s*)$')
        self.table_structure = re.compile(r'^[:\s\-|]*$')

    def parse_to_segments(self, text: str):
        lines = text.split('\n')
        segments = []
        in_code_block = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # 状态切换：代码块
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            # 过滤逻辑：如果满足以下条件，则该行不需要翻译
            if in_code_block or self.ignore_pattern.match(stripped):
                continue
            if self.table_structure.match(stripped) and '|' in line:
                continue
            
            # 过滤掉纯符号行
            content_only = re.sub(r'[#*`\-_\[\]()>]', '', stripped).strip()
            if not content_only:
                continue

            # 只有通过过滤的行才作为译文对象
            segments.append({
                "id": i,
                "source": line,
                "target": ""
            })
            
        return segments

    def render_translation(self, original_text: str, translations: dict):
        """
        全量还原逻辑：
        1. 遍历原文的每一行。
        2. 如果该行的行号在 translations 字典中，则替换为译文。
        3. 如果不在（说明是代码块、符号行或空行），则保留原文。
        """
        lines = original_text.split('\n')
        result = []
        
        for i, line in enumerate(lines):
            key = str(i) # 前端传回的 key 是字符串格式的行号
            if key in translations and translations[key]:
                # 这里的逻辑是：如果用户提供了译文，我们就使用译文
                # 为了防止 AI 丢失 Markdown 符号，建议在导出时做符号补全
                result.append(translations[key])
            else:
                # 没有任何匹配，说明这一行是结构符号或不需要翻译的内容，直接放回原文
                result.append(line)
                
        return '\n'.join(result)