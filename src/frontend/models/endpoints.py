""" Endpoint Locations """
from enum import Enum

from src.frontend import CONFIG

class APIEndpoint(Enum):
    OLLAMA_CHAT = (CONFIG["endpoints"]["ollama"], "Ollama LLM endpoint")
    RAG_SERVICE = (CONFIG["endpoints"]["rag_service"], "RAG document similarity service")

    def __init__(self, url: str, description: str):
        self.url = url
        self.description = description
