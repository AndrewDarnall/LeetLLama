""" RAG Microservice Client """
from httpx import AsyncClient
from src.frontend.models.endpoints import APIEndpoint
import html
import re

async def fetch_external_context(prompt: str) -> str:
    async with AsyncClient() as client:
        try:
            resp = await client.post(APIEndpoint.RAG_SERVICE.url, json={"query": prompt})
            resp.raise_for_status()
            data = resp.json()  # If your httpx version supports this synchronously. Otherwise: await resp.json()

            print(f"RAG Response:\n{data}")

            return data

        except Exception as e:
            print(f"❌ RAG fetch failed: {e}")
            raise
