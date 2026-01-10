import tempfile
import os
import markdown
from docx import Document
import fitz  # PyMuPDF

class DocumentService:
    async def parse_document(self, file):
        """
        解析不同格式的文档，提取文本内容
        """
        filename = file.filename.lower()
        
        if filename.endswith(".md"):
            # 解析 Markdown 文件
            content = await file.read()
            return content.decode("utf-8")
        
        elif filename.endswith(".docx"):
            # 解析 DOCX 文件
            content = await file.read()
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                doc = Document(temp_file_path)
                text = []
                for paragraph in doc.paragraphs:
                    text.append(paragraph.text)
                return "\n".join(text)
            finally:
                os.unlink(temp_file_path)
        
        elif filename.endswith(".pdf"):
            # 解析 PDF 文件
            content = await file.read()
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            try:
                doc = fitz.open(temp_file_path)
                text = []
                for page in doc:
                    text.append(page.get_text())
                return "\n".join(text)
            finally:
                os.unlink(temp_file_path)
        
        else:
            # 尝试以纯文本方式解析
            content = await file.read()
            try:
                return content.decode("utf-8")
            except:
                return "Unsupported file format"
    
    async def export_document(self, project_id: int, format: str = "markdown"):
        """
        导出翻译后的文档
        """
        # 模拟导出功能
        # 实际项目中，这里应该从数据库获取项目的翻译内容
        
        # 模拟翻译内容
        content = """# 翻译示例文档

## 第一部分
Hello, how are you?
你好，你好吗？

## 第二部分
I am fine, thank you.
我很好，谢谢你。
"""
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False, mode="w", encoding="utf-8") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        return temp_file_path