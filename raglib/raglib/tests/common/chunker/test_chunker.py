""" Vanilla Chunker Unit Test """
import os
import tempfile
from pathlib import Path
import pytest

from raglib.common.chunker.vanilla_chunker import MarkdownDirectoryChunker
from raglib.common.chunker.base import Chunk


# Subclass to stub out chunk_text logic for testing
class DummyChunker(MarkdownDirectoryChunker):
    def chunk_text(self, text):
        # Simple deterministic chunking for testing: 10 chars each
        for i in range(0, len(text), 10):
            yield i // 10, text[i:i+10], i, i+10


def create_md_file(dir_path: Path, filename: str, content: str):
    file_path = dir_path / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def test_raises_error_when_directory_missing():
    with pytest.raises(ValueError, match="No directory path was provided."):
        DummyChunker(None)


def test_raises_error_when_path_invalid():
    with pytest.raises(ValueError, match="is not a valid directory"):
        DummyChunker("/some/invalid/path")


def test_raises_error_when_no_md_files():
    with tempfile.TemporaryDirectory() as tmpdirname:
        Path(tmpdirname, "not_markdown.txt").write_text("Just text")
        with pytest.raises(ValueError, match="No Markdown"):
            DummyChunker(tmpdirname)


def test_generate_chunks_returns_expected_chunks():
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        create_md_file(tmpdir, "sample.md", "This is a test markdown file with multiple sentences.")

        chunker = DummyChunker(tmpdirname)
        chunks = list(chunker.generate_chunks())

        assert len(chunks) > 0
        for idx, chunk in enumerate(chunks):
            assert isinstance(chunk, Chunk)
            assert chunk.source_file == "sample.md"
            assert chunk.chunk_index == idx
            assert chunk.start_char < chunk.end_char
            assert chunk.content.strip() != ""
