from elasticsearch import Elasticsearch
from app.config import settings

class ElasticsearchClient:
    def __init__(self):
        self.client = Elasticsearch(settings.ELASTICSEARCH_URL)
    
    def create_index(self, index_name: str):
        """
        创建索引
        """
        if not self.client.indices.exists(index=index_name):
            self.client.indices.create(
                index=index_name,
                body={
                    "mappings": {
                        "properties": {
                            "source_text": {
                                "type": "text",
                                "analyzer": "standard"
                            },
                            "target_text": {
                                "type": "text",
                                "analyzer": "standard"
                            },
                            "source_language": {
                                "type": "keyword"
                            },
                            "target_language": {
                                "type": "keyword"
                            },
                            "created_at": {
                                "type": "date"
                            }
                        }
                    }
                }
            )
    
    def index_document(self, index_name: str, document: dict):
        """
        索引文档
        """
        return self.client.index(index=index_name, body=document)
    
    def search(self, index_name: str, query: str, source_language: str, target_language: str, size: int = 5):
        """
        搜索文档
        """
        return self.client.search(
            index=index_name,
            body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "source_text": {
                                        "query": query,
                                        "fuzziness": "AUTO"
                                    }
                                }
                            },
                            {
                                "term": {
                                    "source_language": source_language
                                }
                            },
                            {
                                "term": {
                                    "target_language": target_language
                                }
                            }
                        ]
                    }
                },
                "size": size
            }
        )

# 创建全局实例
es_client = ElasticsearchClient()