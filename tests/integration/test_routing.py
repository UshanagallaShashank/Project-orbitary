# test_routing.py — integration tests for orchestrator routing + memory flow

import json
import pytest
from unittest.mock import MagicMock, patch

from agents.orchestrator import AGENT_REGISTRY


@pytest.fixture
def orchestrator():
    with patch("agents.orchestrator.OrchestratorAgent._build_client", return_value=MagicMock()):
        from agents.orchestrator import OrchestratorAgent
        return OrchestratorAgent()


@pytest.fixture
def memory():
    with patch("memory.redis_store.redis.Redis") as mock_redis:
        mock_redis.return_value = MagicMock()
        from agents.memory_agent import MemoryAgent
        a = MemoryAgent()
        a._redis._client = mock_redis.return_value
        return a


# Every known intent routes to exactly one agent
def test_all_known_intents_route_to_one_agent(orchestrator):
    for intent in AGENT_REGISTRY:
        result = orchestrator.route(intent, {})
        assert len(result) == 1


# UNKNOWN never routes to an agent
def test_unknown_intent_routes_to_nothing(orchestrator):
    assert orchestrator.route("UNKNOWN", {}) == []


# run output has all required keys
def test_run_output_shape(orchestrator):
    orchestrator._client.models.generate_content.return_value = MagicMock(text="DSA")
    result = orchestrator.run("explain heaps", {"session_id": "i1"})
    assert set(result.keys()) >= {"intent", "agents", "response"}


# Memory read before orchestration returns safely
def test_memory_read_before_orchestration(orchestrator, memory):
    memory._redis._client.get.return_value = None
    ctx = memory.read("i2", "last_intent")
    result = orchestrator.run("explain quicksort", {"session_id": "i2", "prior": ctx})
    assert "intent" in result


# Write then read cycle reflects stored value
def test_memory_write_read_cycle(memory):
    memory._redis._client.setex.return_value = 1
    memory._redis._client.get.return_value = '"trees"'
    memory.write("i3", "topic", "trees")
    val = memory.read("i3", "topic")
    assert val == "trees"


# Semantic search always returns a list
def test_memory_search_returns_list(memory):
    result = memory.semantic_search("dynamic programming")
    assert isinstance(result, list)


# Lambda handler returns 200 with correct shape
def test_lambda_handler_response_shape():
    with patch("agents.orchestrator.OrchestratorAgent._build_client", return_value=MagicMock()):
        with patch("memory.redis_store.redis.Redis", return_value=MagicMock()):
            from infra.lambda_handler import handler
            event = {"body": json.dumps({"session_id": "i4", "text": "what is a heap"})}
            response = handler(event, {})
            assert response["statusCode"] == 200
            body = json.loads(response["body"])
            assert "intent" in body


# Lambda handler with missing text returns 400
def test_lambda_handler_missing_text():
    with patch("agents.orchestrator.OrchestratorAgent._build_client", return_value=MagicMock()):
        with patch("memory.redis_store.redis.Redis", return_value=MagicMock()):
            from infra.lambda_handler import handler
            event = {"body": json.dumps({"session_id": "i5"})}
            response = handler(event, {})
            assert response["statusCode"] == 400
