import os
from pathlib import Path
from typing import Generator
from dataclasses import dataclass

# === SETTINGS ===
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
MARKDOWN_DIR = "knowledge_base/"  # folder containing .md files

# === DATA STRUCTURE ===
@dataclass
class Chunk:
    content: str
    source_file: str
    chunk_index: int
    start_char: int
    end_char: int

# === CHUNKING FUNCTION ===
def chunk_text(text: str, chunk_size: int, overlap: int) -> Generator[tuple[int, str, int, int], None, None]:
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        yield idx, text[start:end], start, end
        start += chunk_size - overlap
        idx += 1

# === MAIN PROCESSING GENERATOR ===
def process_markdown_directory(directory: str) -> Generator[Chunk, None, None]:
    for filepath in Path(directory).rglob("*.md"):
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            for chunk_index, chunk_text_str, start_char, end_char in chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP):
                yield Chunk(
                    content=chunk_text_str,
                    source_file=os.path.basename(filepath),
                    chunk_index=chunk_index,
                    start_char=start_char,
                    end_char=end_char
                )

# === EXAMPLE CONSUMPTION LAYER (Next Layer) ===
def consume_chunks():
    for chunk in process_markdown_directory(MARKDOWN_DIR):
        # Replace this line with NLP processing or ingestion into a vector DB
        print(f"[{chunk.source_file} - #{chunk.chunk_index}] ({chunk.start_char}-{chunk.end_char}): {chunk.content[:60]}...")

# === RUN (for testing) ===
if __name__ == "__main__":
    consume_chunks()
