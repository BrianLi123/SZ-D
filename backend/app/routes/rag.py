# backend/api/routers/rag.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
import tempfile
import os
from ..api.models import (
    DocumentUploadRequest,
    SearchRequest,
    SearchResult,
    HealthCheckResponse
)
from ..rag.data_loader import load_and_index_documents
from ..rag.vector_db import build_vector_store
from ..rag.advanced_retriever import AdvancedRetriever


router = APIRouter(prefix="/rag", tags=["RAG Operations"])

# 依赖项提前定义
def get_vector_store(index_name: str):
    return build_vector_store(index_name)

def get_retriever(
    search_request: SearchRequest,
    vector_store = Depends(get_vector_store)
):
    return AdvancedRetriever(
        vector_store=vector_store,
        company=search_request.company
    )


@router.post("/upload/", summary="上传并索引文档")
async def upload_documents(
    files: List[UploadFile] = File(...),
    company: str = "default",
    index_name: str = "default-index"
):
    """处理多文件上传和索引"""
    try:
        # 保存上传文件到临时目录
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            file_paths.append(file_path)
        
        # 加载和索引文档
        count = load_and_index_documents(
            file_paths=file_paths,
            index_name=index_name,
            company=company
        )
        
        return {"message": f"成功索引 {count} 个文档", "index": index_name}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/", response_model=List[SearchResult])
async def search_documents(
    request: SearchRequest,
    retriever: AdvancedRetriever = Depends(get_retriever)
):
    """执行高级文档检索"""
    try:
        results = retriever.get_relevant_documents(request.query)
        return [
            SearchResult(
                content=doc.page_content,
                score=doc.metadata["score"],
                metadata=doc.metadata
            )
            for doc in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }