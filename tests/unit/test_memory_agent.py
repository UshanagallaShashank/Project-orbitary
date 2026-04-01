# test_memory_agent.py — unit tests for MemoryAgent with mocked Redis

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def agent():
    with patch("memory.redis_store.redis.Redis") as mock_redis:
        mock_redis.return_value = MagicMock()
        from agents.memory_agent import MemoryAgent
        a = MemoryAgent()
        a._redis._client = mock_redis.return_value
        return a


# read — happy path: returns parsed value from Redis
def test_read_returns_value(agent):
    agent._redis._client.get.return_value = '"DSA"'
    result = agent.read("s1", "last_intent")
    assert result == "DSA"


# read — edge case: missing key returns None
def test_read_missing_key_returns_none(agent):
    agent._redis._client.get.return_value = None
    result = agent.read("s1", "missing")
    assert result is None


# write — happy path: Redis setex returns 1 → True
def test_write_returns_true(agent):
    agent._redis._client.setex.return_value = 1
    result = agent.write("s1", "last_intent", "MENTOR")
    assert result is True


# write — failure: Redis setex returns 0 → False
def test_write_returns_false_on_failure(agent):
    agent._redis._client.setex.return_value = 0
    result = agent.write("s1", "key", "val")
    assert result is False


# delete — happy path: key existed → True
def test_delete_existing_key(agent):
    agent._redis._client.delete.return_value = 1
    result = agent.delete("s1", "last_intent")
    assert result is True


# delete — edge case: key did not exist → False
def test_delete_missing_key(agent):
    agent._redis._client.delete.return_value = 0
    result = agent.delete("s1", "ghost")
    assert result is False


# get_all_keys — returns list with namespace stripped
def test_get_all_keys_strips_prefix(agent):
    agent._redis._client.keys.return_value = ["orbit:s1:topic", "orbit:s1:intent"]
    result = agent.get_all_keys("s1")
    assert "topic" in result
    assert "intent" in result


# run — unknown action returns error dict
def test_run_unknown_action(agent):
    result = agent.run("explode", {})
    assert "error" in result


# run — read dispatches correctly
def test_run_read_dispatches(agent):
    agent._redis._client.get.return_value = '"trees"'
    result = agent.run("read", {"session_id": "s1", "key": "topic"})
    assert result["value"] == "trees"


# run — write dispatches correctly
def test_run_write_dispatches(agent):
    agent._redis._client.setex.return_value = 1
    result = agent.run("write", {"session_id": "s1", "key": "k", "value": "v"})
    assert result["ok"] is True
