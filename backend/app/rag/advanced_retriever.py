# backend/rag/advanced_retriever.py
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List, Optional, Dict, Any
from rag.vector_db import init_vector_store, create_documents_from_results

# 增强的检索器实现（支持类别过滤）
class AdvancedRetriever(BaseRetriever):
    def __init__(self):
        super().__init__()
        
    def _get_relevant_documents(
        self, 
        query: str,
        *,
        top_k: int = 5,
        score_threshold: float = 0.7,
        category: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Document]:
        index_name = "brian-test"
        vector_store = init_vector_store(index_name)

        # 构建类别过滤器
        search_filter = f"category eq '{category}'" if category else None
        
        results = vector_store.hybrid_search(
            query=query,
            k=top_k,
            filter=search_filter,
            score_threshold=score_threshold,
        )
        print(f"检索到{len(results)}条结果（类别过滤：{category or '无'}）")
        return results

    async def _aget_relevant_documents(
        self, 
        query: str,
        *,
        top_k: int = 5,
        category: Optional[str] = None,
        **kwargs: Any,
    ) -> List[Document]:
        index_name = "brian-test"
        vector_store = init_vector_store(index_name)

        # 构建类别过滤器
        search_filter = f"category eq '{category}'" if category else None
        
        # 异步搜索（假设AzureSearch支持异步接口）
        results = vector_store.similarity_search_with_score(
            query=query,
            k=top_k,
            filters=search_filter,
        )
        print(f"异步检索到{len(results)}条结果（类别过滤：{category or '无'}）")
        return results