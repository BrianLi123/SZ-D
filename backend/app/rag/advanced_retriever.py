# backend/rag/advanced_retriever.py
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from typing import List, Optional, Dict, Any
from rag.vector_db import init_vector_store, create_documents_from_results

class AdvancedRetriever(BaseRetriever):
    def __init__(self):
        super().__init__()
        # self.company_filter = f"company eq '{company}'" if company else None
        
    def _get_relevant_documents(
        self, 
        query: str,
        *,
        top_k: int = 5,
        score_threshold: float = 0.7,
        **kwargs: Any,
    ) -> List[Document]:
        index_name = "brian-test"
        vector_store = init_vector_store(index_name)

        # 打印调试信息
        # print(f"当前过滤器: {self.company_filter}")  # 检查实际生成的filter

        results = vector_store.hybrid_search(
            query=query,
            k=top_k,
            # filters=self.company_filter,  # 现在这里会是类似 "company eq 'xxx'" 的合法表达式
            score_threshold=score_threshold,
        )
        return results

    # async def _aget_relevant_documents(self, *args, **kwargs):
    #     # 异步实现（如果需要）
    #     return await self.vector_store.async_hybrid_search(*args, **kwargs)