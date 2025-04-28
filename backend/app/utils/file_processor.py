from pathlib import Path

from langchain.document_loaders import (
    PyPDFLoader, Docx2txtLoader, 
    UnstructuredPowerPointLoader, TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import settings
import hashlib

SUPPORTED_EXT = {
    ".pdf": PyPDFLoader,
    ".docx": Docx2txtLoader,
    ".pptx": UnstructuredPowerPointLoader,
    ".txt": TextLoader
}

def process_file(file_path: str):
    """处理单个文件并返回分块文档"""
    file_ext = Path(file_path).suffix.lower()
    if file_ext not in SUPPORTED_EXT:
        raise ValueError(f"Unsupported file type: {file_ext}")

    loader = SUPPORTED_EXT[file_ext](file_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        add_start_index=True
    )
    splits = text_splitter.split_documents(docs)
    
    # 添加文档哈希用于版本控制
    doc_hash = hashlib.md5(open(file_path, "rb").read()).hexdigest()
    for split in splits:
        split.metadata["doc_hash"] = doc_hash

    # 保存原始文本用于BM25
    processed_dir = settings.DATA_DIR / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    text_content = "\n".join([doc.page_content for doc in splits])
    output_path = processed_dir / f"{doc_hash}.txt"
    output_path.write_text(text_content)    
    
    return splits