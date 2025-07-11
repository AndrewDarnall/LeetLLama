""" BAAI - BGE Concrete Embedder Component """
from typing import List

from sentence_transformers import SentenceTransformer

from raglib.common.embedder.base import BaseTextEmbedder

class BGETextEmbedder(BaseTextEmbedder):
    """
    Embeds text using the BAAI/bge-large-en model via SentenceTransformers.
    """

    def __init__(self, model_name: str = "BAAI/bge-large-en", normalize: bool = True):
        self.model = SentenceTransformer(model_name)
        self.normalize = normalize

    def embed(self, text: str) -> List[float]:
        """
        Returns the embedding for the given input string.
        """
        if self.normalize:
            return self.model.encode(text, normalize_embeddings=True).tolist()
        else:
            return self.model.encode(text).tolist()
