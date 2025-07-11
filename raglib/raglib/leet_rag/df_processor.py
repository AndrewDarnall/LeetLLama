""" Leetcode Dataset Processor """
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from pandas import DataFrame, read_json


class BaseDataFrameProcessor(ABC):
    """
    Abstract base class for processing structured tabular data (e.g. from JSONL, CSV).
    """

    def __init__(self, source_path: Union[str, Path]):
        self.source_path = Path(source_path)

        if not self.source_path.exists():
            raise FileNotFoundError(f"Input file not found: {self.source_path}")
        if not self.source_path.is_file():
            raise ValueError(f"Provided path is not a file: {self.source_path}")

    @abstractmethod
    def load_and_process(self) -> DataFrame:
        """
        Load and process the input file, returning a processed DataFrame.
        """
        pass


class JsonlCodeDataFrameProcessor(BaseDataFrameProcessor):
    """
    Concrete DataFrame processor for JSONL files with 'content', 'python', and 'id' columns.
    """

    def load_and_process(self) -> DataFrame:
        # Load the file into a DataFrame
        df = read_json(self.source_path, lines=True)

        # Drop the 'id' column if it exists
        if 'id' in df.columns:
            df = df.drop(columns=['id'])

        # Select only the desired columns
        expected_columns = ["content", "python"]
        missing = [col for col in expected_columns if col not in df.columns]
        if missing:
            raise ValueError(f"Missing expected columns in JSONL: {missing}")

        return df[expected_columns].copy()
