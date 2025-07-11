""" Milvus Vector Store Connector Unit Test """
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from raglib.common.vstore_connector.milvus_connector import MilvusConnector


@pytest.fixture
def mock_milvus():
    with patch("raglib.common.vstore_connector.milvus_connector.connections") as mock_connections, \
         patch("raglib.common.vstore_connector.milvus_connector.utility") as mock_utility, \
         patch("raglib.common.vstore_connector.milvus_connector.Collection") as mock_collection_class, \
         patch("raglib.common.vstore_connector.milvus_connector.FieldSchema"), \
         patch("raglib.common.vstore_connector.milvus_connector.CollectionSchema"), \
         patch("raglib.common.vstore_connector.milvus_connector.DataType"):
        
        mock_collection = MagicMock()
        mock_collection_class.return_value = mock_collection
        mock_utility.has_collection.return_value = False
        
        yield {
            "connections": mock_connections,
            "utility": mock_utility,
            "Collection": mock_collection,
        }


def test_connect_creates_collection(mock_milvus):
    connector = MilvusConnector(host="localhost", port="19530", collection_name="test_collection")
    connector.connect()

    mock_milvus["connections"].connect.assert_called_once_with(alias="default", host="localhost", port="19530")
    assert connector.connected is True
    assert mock_milvus["Collection"].load.called


def test_insert_embedding_success(mock_milvus):
    connector = MilvusConnector(host="localhost", port="19530", collection_name="test_collection", dim=3)
    connector.collection = MagicMock()

    valid_embedding = np.array([0.1, 0.2, 0.3])
    connector.insert_embedding(valid_embedding, id=123)

    connector.collection.insert.assert_called_once_with([[123], [valid_embedding.tolist()]])


def test_insert_embedding_invalid_dim_raises(mock_milvus):
    connector = MilvusConnector(host="localhost", port="19530", collection_name="test_collection", dim=3)
    connector.collection = MagicMock()

    invalid_embedding = np.array([0.1, 0.2])  # wrong dim
    with pytest.raises(ValueError, match="Embedding dim 2 does not match expected 3"):
        connector.insert_embedding(invalid_embedding, id=456)


def test_similarity_search_filters_by_threshold(mock_milvus):
    connector = MilvusConnector(host="localhost", port="19530", collection_name="test_collection", dim=3)
    
    mock_hit = MagicMock()
    mock_hit.id = 99
    mock_hit.score = 0.85
    
    mock_low_hit = MagicMock()
    mock_low_hit.id = 88
    mock_low_hit.score = 0.5

    mock_results = [[mock_hit, mock_low_hit]]

    mock_collection = MagicMock()
    mock_collection.search.return_value = mock_results
    connector.collection = mock_collection

    embedding = np.array([0.1, 0.2, 0.3])
    results = connector.similarity_search(embedding, top_k=2, threshold=0.8)

    assert len(results) == 1
    assert results[0]["id"] == 99
    assert results[0]["score"] == 0.85


def test_close_disconnects(mock_milvus):
    connector = MilvusConnector(host="localhost", port="19530", collection_name="test_collection")
    connector.connected = True

    connector.close()

    mock_milvus["connections"].disconnect.assert_called_once_with("default")
    assert not connector.connected
