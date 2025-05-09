# backend/rag/data_loader.py
import os
from typing import List, Optional, Dict
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.vector_db import init_vector_store
SUPPORTED_EXTENSIONS = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".txt": TextLoader,
}

def load_and_index_documents(
    file_paths: List[str],
    index_name: str,
    company: Optional[str] = None,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    additional_metadata: Optional[Dict] = None
) -> int:
    """文档加载与索引增强版"""
    vector_store = init_vector_store(index_name)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    all_docs = []
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[-1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue
            
        loader = SUPPORTED_EXTENSIONS[ext](file_path)
        docs = loader.load()
        
        # 增强元数据
        for doc in docs:
            doc.metadata.update({
                "company": company,
                "source": file_path,
                **(additional_metadata or {})
            })
        
        split_docs = text_splitter.split_documents(docs)
        all_docs.extend(split_docs)
    
    if all_docs:
        vector_store.add_documents(all_docs)
    return len(all_docs)