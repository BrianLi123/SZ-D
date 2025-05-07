# backend/rag/advanced_retriever.py
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List, Optional, Dict, Any

class AdvancedRetriever(BaseRetriever):
    def __init__(self, vector_store, company: Optional[str] = None):
        self.vector_store = vector_store
        self.company_filter = f"company eq '{company}'" if company else None
        
    def _get_relevant_documents(
        self, 
        query: str,
        *,
        top_k: int = 5,
        score_threshold: float = 0.7,
        **kwargs: Any,
    ) -> List[Document]:
        # 使用混合搜索（向量+关键词）
        results = self.vector_store.hybrid_search(
            query=query,
            k=top_k,
            filters=self.company_filter,
            score_threshold=score_threshold,
        )
        return results

    async def _aget_relevant_documents(self, *args, **kwargs):
        # 异步实现（如果需要）
        return await self.vector_store.async_hybrid_search(*args, **kwargs)