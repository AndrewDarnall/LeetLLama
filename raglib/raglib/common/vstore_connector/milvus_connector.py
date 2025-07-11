""" Concrete Milvus Vector Store Connector """
from typing import List

from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import numpy as np

from raglib.common.vstore_connector.base import BaseVectorStoreConnector


class MilvusConnector(BaseVectorStoreConnector):
    def __init__(self, host: str, port: str, collection_name: str, dim: int = 768):
        self.host = host
        self.port = port
        self.collection_name = collection_name
        self.dim = dim
        self.collection = None
        self.connected = False

    def connect(self):
        if not self.connected:
            connections.connect(alias="default", host=self.host, port=self.port)
            self.connected = True
            print(f"✅ Connected to Milvus at {self.host}:{self.port}")
        self.ensure_collection(self.collection_name, self.dim)

    def ensure_collection(self, collection_name: str, dim: int):
        if not utility.has_collection(collection_name):
            print(f"📁 Creating new collection: {collection_name}")
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
            ]
            schema = CollectionSchema(fields, description="Embedding collection")
            self.collection = Collection(name=collection_name, schema=schema)
            index_params = {
                "index_type": "IVF_FLAT",  # You can change to GPU-specific like IVF_PQ, etc.
                "metric_type": "COSINE",
                "params": {"nlist": 128}
            }
            self.collection.create_index(field_name="embedding", index_params=index_params)
            self.collection.load()
        else:
            self.collection = Collection(name=collection_name)
            self.collection.load()
            print(f"📂 Using existing collection: {collection_name}")

    def insert_embedding(self, embedding: np.ndarray, id: int):
        if embedding.shape[-1] != self.dim:
            raise ValueError(f"Embedding dim {embedding.shape[-1]} does not match expected {self.dim}")
        self.collection.insert([[id], [embedding.tolist()]])
        print(f"📥 Inserted embedding with ID {id}")

    def similarity_search(self, embedding: np.ndarray, top_k: int = 5, threshold: float = 0.8) -> List[dict]:
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

        results = self.collection.search(
            data=[embedding.tolist()],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["id"]
        )

        output = []
        for hit in results[0]:
            if hit.score >= threshold:
                output.append({
                    "id": hit.id,
                    "score": hit.score
                })
        print(f"🔍 Found {len(output)} similar embeddings above threshold {threshold}")
        return output

    def close(self):
        if self.connected:
            connections.disconnect("default")
            self.connected = False
            print("🔌 Disconnected from Milvus")
