""" Base Vector Store Connector """
from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BaseVectorStoreConnector(ABC):
    """
    Abstract base class for vector store connectors.
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def ensure_collection(self, collection_name: str, dim: int):
        pass

    @abstractmethod
    def insert_embedding(self, embedding: np.ndarray, id: int):
        pass

    @abstractmethod
    def similarity_search(self, embedding: np.ndarray, top_k: int = 5, threshold: float = 0.8) -> List[dict]:
        pass

    @abstractmethod
    def close(self):
        pass
