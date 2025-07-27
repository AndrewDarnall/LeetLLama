""" Web RAG API Endpoint """
from fastapi import FastAPI, HTTPException

from .models.io import RAGRequest, RAGResponse
from .rag_service import handle_rag_query



app = FastAPI(title="LeetLLaMA RAG Microservice")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Web-RAG service is operational."}


@app.post("/api/rag-retrieve", response_model=RAGResponse)
async def rag_retrieve(request: RAGRequest):
    return handle_rag_query(request)