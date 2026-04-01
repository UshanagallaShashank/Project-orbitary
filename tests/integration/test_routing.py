# test_routing.py — integration tests for orchestrator routing + memory stubs

import pytest

from agents.orchestrator import OrchestratorAgent, AGENT_REGISTRY
from agents.memory_agent import MemoryAgent


@pytest.fixture
def orchestrator():
    return OrchestratorAgent()


@pytest.fixture
def memory():
    return MemoryAgent()


# Routing — each known intent maps to exactly one agent
def test_all_known_intents_route_to_an_agent(orchestrator):
    for intent in AGENT_REGISTRY:
        result = orchestrator.route(intent, {})
        assert len(result) == 1


# Routing — UNKNOWN never routes to an agent
def test_unknown_intent_routes_to_nothing(orchestrator):
    result = orchestrator.route("UNKNOWN", {})
    assert result == []


# Routing — run output includes intent and agents
def test_run_output_shape(orchestrator):
    result = orchestrator.run("show my calendar for tomorrow", {"session_id": "int-1"})
    assert set(result.keys()) >= {"intent", "agents", "response"}


# Memory + Orchestrator — memory read before orchestration returns safely
def test_memory_read_before_orchestration(orchestrator, memory):
    ctx = memory.read("int-2", "last_intent")
    result = orchestrator.run("explain quicksort", {"session_id": "int-2", "prior": ctx})
    assert "intent" in result


# Memory — write then read cycle (stub: always None, confirms no crash)
def test_memory_write_read_cycle(memory):
    memory.write("int-3", "topic", "trees")
    val = memory.read("int-3", "topic")
    # Stub returns None — just confirm no exception raised
    assert val is None


# Memory — search returns list type regardless of query
def test_memory_search_always_returns_list(memory):
    result = memory.semantic_search("dynamic programming top-down")
    assert isinstance(result, list)


# Lambda handler shape — confirm correct response structure
def test_lambda_handler_response_shape():
    from infra.lambda_handler import handler
    import json
    event = {"body": json.dumps({"session_id": "int-4", "text": "what is a heap"})}
    response = handler(event, {})
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "intent" in body


# Lambda handler — missing text returns 400
def test_lambda_handler_missing_text():
    from infra.lambda_handler import handler
    import json
    event = {"body": json.dumps({"session_id": "int-5"})}
    response = handler(event, {})
    assert response["statusCode"] == 400
