""" Base Class for Embedder Component """
from abc import ABC, abstractmethod
from typing import List


class BaseTextEmbedder(ABC):
    """
    Abstract base class for text embedding models.
    """

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """
        Embed a string of text and return a vector representation.
        """
        pass
