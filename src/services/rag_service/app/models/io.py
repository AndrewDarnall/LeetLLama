""" Pydantic Models """
from pydantic import BaseModel
from typing import Dict

class RAGRequest(BaseModel):
    query: str

class ChunkResult(BaseModel):
    content: str

class RAGResponse(BaseModel):
    results: str
