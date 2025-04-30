# backend/api/models.py
from pydantic import BaseModel
from typing import List, Optional

class DocumentUploadRequest(BaseModel):
    file_paths: List[str]
    company: str
    index_name: str

class SearchRequest(BaseModel):
    query: str
    index_name: str
    company: Optional[str] = None
    top_k: int = 5

class SearchResult(BaseModel):
    content: str
    score: float
    metadata: dict

class HealthCheckResponse(BaseModel):
    status: str
    version: str