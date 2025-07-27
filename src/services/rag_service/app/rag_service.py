""" RAG Pipeline """
import logging
from typing import Dict

from pymilvus import connections, Collection
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from .models.io import RAGRequest, RAGResponse, ChunkResult

from . import CONFIG

# Configuration constants (can move to env or config file)
COLLECTION_NAME = CONFIG["rag_config"]["collection_name"]
TOP_K = CONFIG["rag_config"]["top_k"]
SIMILARITY_THRESHOLD = CONFIG["rag_config"]["score_threshold"]

log = logging.getLogger("Milvus-Search")

# Initialize connection, collection, and embedder once (cache outside function)
MILVUS_HOST, MILVUS_PORT = CONFIG["endpoints"]["milvus"].split("://")[1].split(":")

connections.connect(alias="default", host=MILVUS_HOST, port=int(MILVUS_PORT))
collection = Collection(name=COLLECTION_NAME)
collection.load()

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5",
    normalize=True,
    device="cuda"
)

def handle_rag_query(request: RAGRequest) -> RAGResponse:
    query_text = request.query.strip()
    if not query_text:
        raise ValueError("Query text must not be empty.")

    log.info(f"Received RAG query: {query_text}")

    # 1) Embed query
    query_embedding = embed_model.get_text_embedding(query_text)

    # 2) Search Milvus
    search_params = {
        "metric_type": "IP",
        "params": {"nprobe": 10},
    }

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=TOP_K,
        output_fields=["id", "text"]
    )

    hits = results[0]
    top_results = ""
    for hit in hits:
        top_results += hit.entity.get("text")


    return RAGResponse(results=top_results)
