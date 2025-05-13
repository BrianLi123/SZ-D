# backend/api/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi import UploadFile

class ChatRequest(BaseModel):
    history: List[dict]
    approach: str
    chatroomID: str
    
    # index_name: str = "default-index"

class DocumentUploadRequest(BaseModel):
    company: str
    chatroomID: str
    # index_name: str = "default-index"

class SearchResult(BaseModel):
    content: str
    score: float
    metadata: dict

class HealthCheckResponse(BaseModel):
    status: str
    version: str