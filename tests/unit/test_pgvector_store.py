# test_pgvector_store.py — unit tests for PgVectorStore with mocked DB + Gemini

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def store():
    with patch("memory.pgvector_store.PgVectorStore._build_gemini", return_value=MagicMock()):
        with patch("memory.pgvector_store.psycopg2.connect") as mock_conn:
            mock_conn.return_value.__enter__ = lambda s: mock_conn.return_value
            mock_conn.return_value.__exit__ = MagicMock(return_value=False)
            mock_conn.return_value.cursor.return_value.__enter__ = lambda s: MagicMock()
            mock_conn.return_value.cursor.return_value.__exit__ = MagicMock(return_value=False)
            from memory.pgvector_store import PgVectorStore
            s = PgVectorStore()
            s._mock_conn = mock_conn
            return s


# embed — happy path: returns 768-dim list
def test_embed_returns_768_dim(store):
    mock_result = MagicMock()
    mock_result.embeddings = [MagicMock(values=[0.1] * 768)]
    store._gemini_client.models.embed_content.return_value = mock_result
    result = store.embed("binary search")
    assert len(result) == 768


# embed — no client: returns zero vector
def test_embed_no_client_returns_zeros():
    with patch("memory.pgvector_store.PgVectorStore._build_gemini", return_value=None):
        with patch("memory.pgvector_store.psycopg2.connect"):
            from memory.pgvector_store import PgVectorStore
            s = PgVectorStore()
            result = s.embed("anything")
            assert result == [0.0] * 768


# embed — result is list of floats
def test_embed_returns_list_of_floats(store):
    mock_result = MagicMock()
    mock_result.embeddings = [MagicMock(values=[0.5] * 768)]
    store._gemini_client.models.embed_content.return_value = mock_result
    result = store.embed("trees")
    assert all(isinstance(v, float) for v in result)


# store — happy path: returns True on successful insert
def test_store_returns_true(store):
    with patch.object(store, "embed", return_value=[0.0] * 768):
        with patch.object(store, "_connect") as mock_conn:
            ctx = MagicMock()
            mock_conn.return_value.__enter__ = lambda s: ctx
            mock_conn.return_value.__exit__ = MagicMock(return_value=False)
            result = store.store("binary search is O(log n)", {"topic": "DSA"})
            assert isinstance(result, bool)


# store — failure: DB error returns False
def test_store_returns_false_on_db_error(store):
    with patch.object(store, "embed", return_value=[0.0] * 768):
        with patch.object(store, "_connect", side_effect=Exception("db error")):
            result = store.store("some text", {})
            assert result is False


# search — happy path: returns list of dicts
def test_search_returns_list(store):
    with patch.object(store, "embed", return_value=[0.0] * 768):
        with patch.object(store, "_connect", side_effect=Exception("no db")):
            result = store.search("dynamic programming")
            assert isinstance(result, list)


# search — failure: DB error returns empty list not exception
def test_search_graceful_on_error(store):
    with patch.object(store, "embed", return_value=[0.0] * 768):
        with patch.object(store, "_connect", side_effect=Exception("conn failed")):
            result = store.search("graphs")
            assert result == []


# search — top_k parameter respected
def test_search_top_k_parameter(store):
    with patch.object(store, "embed", return_value=[0.0] * 768):
        with patch.object(store, "_connect", side_effect=Exception("no db")):
            result = store.search("heaps", top_k=5)
            assert isinstance(result, list)
