# test_memory_agent.py — unit tests for MemoryAgent stubs

import pytest

from agents.memory_agent import MemoryAgent


@pytest.fixture
def agent():
    return MemoryAgent()


# read — happy path: stub returns None (not connected yet)
def test_read_returns_none_stub(agent):
    result = agent.read("session-1", "last_intent")

    assert result is None


# write — happy path: stub returns False (not connected yet)
def test_write_returns_false_stub(agent):
    result = agent.write("session-1", "last_intent", "DSA")

    assert result is False


# delete — happy path: stub returns False
def test_delete_returns_false_stub(agent):
    result = agent.delete("session-1", "last_intent")

    assert result is False


# semantic_search — returns empty list in stub
def test_semantic_search_returns_empty_list(agent):
    result = agent.semantic_search("binary search trees")

    assert result == []


# run — unknown action returns error dict
def test_run_unknown_action(agent):
    result = agent.run("explode", {})

    assert "error" in result


# run — read action dispatches correctly
def test_run_read_action(agent):
    result = agent.run("read", {"session_id": "s1", "key": "k1"})

    assert "value" in result


# run — write action dispatches correctly
def test_run_write_action(agent):
    result = agent.run("write", {"session_id": "s1", "key": "k1", "value": "v1"})

    assert "ok" in result


# run — search action dispatches correctly
def test_run_search_action(agent):
    result = agent.run("search", {"query": "arrays"})

    assert "results" in result
