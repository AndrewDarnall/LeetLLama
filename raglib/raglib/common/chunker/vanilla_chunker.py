""" Vanilla Chuncker - Meaning no NLP Applications """
import os
from pathlib import Path
from typing import Generator

from raglib.common.chunker.base import BaseChunker, Chunk


class MarkdownDirectoryChunker(BaseChunker):
    """
    Chunker for Markdown files in a directory. No NLP involved.
    """

    def __init__(self, directory: str, **kwargs):
        super().__init__(**kwargs)

        if not directory:
            raise ValueError("No directory path was provided.")
        
        self.directory = Path(directory)

        if not self.directory.exists() or not self.directory.is_dir():
            raise ValueError(f"Provided path '{directory}' is not a valid directory.")

        if not any(self.directory.rglob("*.md")):
            raise ValueError(f"No Markdown (.md) files found in directory: {directory}")

    def generate_chunks(self) -> Generator[Chunk, None, None]:
        for filepath in self.directory.rglob("*.md"):
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
                for idx, chunk_text, start, end in self.chunk_text(text):
                    yield Chunk(
                        content=chunk_text,
                        source_file=os.path.basename(filepath),
                        chunk_index=idx,
                        start_char=start,
                        end_char=end
                    )
