""" API Service """
from fastapi import FastAPI

api = FastAPI(name="RAG Microservice")


@api.get("/api/health")
async def health_check():
    return {"System Status": "Alive and well!"}