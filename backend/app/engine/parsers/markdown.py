# backend/app/engine/parsers/markdown.py

from markdown_it import MarkdownIt

class MarkdownEngine:
    def __init__(self):
        # 核心修复：使用 "js-default" 替代会报错的 "gfm"
        try:
            self.md = MarkdownIt("js-default", {
                "html": True,
                "linkify": False,
                "typographer": True
            })
        except Exception as e:
            # 增加一个备选方案，如果 js-default 也不行，就用最基础的
            print(f"Markdown 引擎初始化警告: {e}")
            self.md = MarkdownIt() 

    def parse_to_segments(self, content: str):
        # 现在 self.md 已经成功定义，不会再报 AttributeError
        tokens = self.md.parse(content)
        segments = []
        original_lines = content.splitlines()
        
        for i, token in enumerate(tokens):
            if token.type == "inline" and token.map:
                start_line = token.map[0]
                end_line = token.map[1]
                
                safe_start = max(0, start_line)
                safe_end = min(len(original_lines), end_line)
                
                raw_source = "\n".join(original_lines[safe_start:safe_end])
                
                if raw_source.strip():
                    segments.append({
                        "id": i,
                        "source": raw_source,
                        "target": ""
                    })
        return segments

    def render_translation(self, original_content: str, translations: dict):
        tokens = self.md.parse(original_content)
        output = []
        seen_ids = set()

        for i, token in enumerate(tokens):
            if token.type == "inline":
                if i in seen_ids: continue
                
                val = translations.get(str(i)) or translations.get(i)
                
                if val and str(val).strip():
                    output.append(str(val))
                    output.append("\n\n")
                    seen_ids.add(i)
        
        return "".join(output).strip()