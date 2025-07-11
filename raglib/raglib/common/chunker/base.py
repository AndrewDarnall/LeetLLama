""" Base Chunker Class """
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator


@dataclass
class Chunk:
    content: str
    source_file: str
    chunk_index: int
    start_char: int
    end_char: int


class BaseChunker(ABC):
    """
    Abstract base class for all chunking strategies.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> Generator[tuple[int, str, int, int], None, None]:
        """
        Split the text into overlapping chunks.
        """
        start = 0
        idx = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            yield idx, text[start:end], start, end
            start += self.chunk_size - self.chunk_overlap
            idx += 1

    @abstractmethod
    def generate_chunks(self) -> Generator[Chunk, None, None]:
        """
        Abstract method to generate chunks from a source.
        """
        pass
