""" LeetCode Dataset Processor Unit Test """
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from raglib.leet_rag.df_processor import JsonlCodeDataFrameProcessor


@pytest.fixture
def valid_jsonl_file():
    content = '{"id": 1, "content": "Question 1", "python": "print(1)"}\n' \
              '{"id": 2, "content": "Question 2", "python": "print(2)"}\n'
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".jsonl", delete=False) as tmpfile:
        tmpfile.write(content)
        tmpfile.flush()
        yield tmpfile.name
        Path(tmpfile.name).unlink()


@pytest.fixture
def missing_column_jsonl_file():
    content = '{"id": 1, "content": "Only content"}\n'
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".jsonl", delete=False) as tmpfile:
        tmpfile.write(content)
        tmpfile.flush()
        yield tmpfile.name
        Path(tmpfile.name).unlink()


def test_valid_jsonl_processing(valid_jsonl_file):
    processor = JsonlCodeDataFrameProcessor(valid_jsonl_file)
    df = processor.load_and_process()

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["content", "python"]
    assert len(df) == 2
    assert df.iloc[0]["content"] == "Question 1"
    assert df.iloc[1]["python"] == "print(2)"


def test_missing_column_raises(missing_column_jsonl_file):
    processor = JsonlCodeDataFrameProcessor(missing_column_jsonl_file)
    with pytest.raises(ValueError, match="Missing expected columns"):
        processor.load_and_process()


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        JsonlCodeDataFrameProcessor("non_existent_file.jsonl")


def test_path_is_not_file(tmp_path):
    directory = tmp_path / "a_dir"
    directory.mkdir()
    with pytest.raises(ValueError, match="is not a file"):
        JsonlCodeDataFrameProcessor(directory)
