""" BAAI BGE Embedder Unit Test """
import pytest
from unittest.mock import patch, MagicMock

import numpy as np

from raglib.common.embedder.bge_embedder import BGETextEmbedder



@patch("raglib.common.embedder.bge_embedder.SentenceTransformer")
def test_embed_with_normalization(mock_model_class):
    mock_model = MagicMock()
    # Return a NumPy array instead of list
    mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])
    mock_model_class.return_value = mock_model

    embedder = BGETextEmbedder(model_name="fake-model", normalize=True)
    result = embedder.embed("Test input")

    mock_model.encode.assert_called_once_with("Test input", normalize_embeddings=True)
    assert isinstance(result, list)
    assert result == [0.1, 0.2, 0.3]



@patch("raglib.common.embedder.bge_embedder.SentenceTransformer")
def test_embed_without_normalization(mock_model_class):
    mock_model = MagicMock()
    mock_model.encode.return_value = np.array([0.4, 0.5, 0.6])  # Use np.array here
    mock_model_class.return_value = mock_model

    embedder = BGETextEmbedder(model_name="fake-model", normalize=False)
    result = embedder.embed("Another input")

    mock_model.encode.assert_called_once_with("Another input")
    assert isinstance(result, list)
    assert result == [0.4, 0.5, 0.6]
