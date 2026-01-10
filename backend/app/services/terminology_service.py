from typing import List, Optional
from app.schemas.terminology import TermCreate, TermResponse, TermList

class TerminologyService:
    def __init__(self):
        # 这里可以初始化术语库连接
        self.terms = []
        self.term_id_counter = 1

    async def create_term(self, term: TermCreate):
        # 模拟创建术语
        term_data = {
            "id": self.term_id_counter,
            **term.model_dump()
        }
        self.term_id_counter += 1
        self.terms.append(term_data)
        return TermResponse(**term_data)

    async def get_terms(self, source_language: Optional[str] = None, target_language: Optional[str] = None, domain: Optional[str] = None):
        # 模拟获取术语列表，支持筛选
        filtered_terms = self.terms
        
        if source_language:
            filtered_terms = [term for term in filtered_terms if term["source_language"] == source_language]
        
        if target_language:
            filtered_terms = [term for term in filtered_terms if term["target_language"] == target_language]
        
        if domain:
            filtered_terms = [term for term in filtered_terms if term["domain"] == domain]
        
        return [
            TermList(
                id=term["id"],
                source_term=term["source_term"],
                target_term=term["target_term"],
                source_language=term["source_language"],
                target_language=term["target_language"],
                domain=term["domain"]
            )
            for term in filtered_terms
        ]

    async def get_term(self, term_id: int):
        # 模拟获取术语详情
        for term in self.terms:
            if term["id"] == term_id:
                return TermResponse(**term)
        raise Exception(f"Term with id {term_id} not found")

    async def update_term(self, term_id: int, term: TermCreate):
        # 模拟更新术语
        for i, existing_term in enumerate(self.terms):
            if existing_term["id"] == term_id:
                updated_term = {
                    "id": term_id,
                    **term.model_dump()
                }
                self.terms[i] = updated_term
                return TermResponse(**updated_term)
        raise Exception(f"Term with id {term_id} not found")

    async def delete_term(self, term_id: int):
        # 模拟删除术语
        for i, term in enumerate(self.terms):
            if term["id"] == term_id:
                self.terms.pop(i)
                return
        raise Exception(f"Term with id {term_id} not found")