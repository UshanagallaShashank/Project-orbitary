# test_orchestrator.py — unit tests for OrchestratorAgent

import pytest

from agents.orchestrator import OrchestratorAgent, AGENT_REGISTRY, INTENT_LABELS


@pytest.fixture
def agent():
    return OrchestratorAgent()


# classify_intent — happy path
def test_classify_intent_returns_string(agent):
    result = agent.classify_intent("explain binary search")

    assert isinstance(result, str)


# classify_intent — edge case: empty string
def test_classify_intent_empty_text(agent):
    result = agent.classify_intent("")

    assert result in INTENT_LABELS


# classify_intent — failure: non-string input falls back
def test_classify_intent_none_input(agent):
    result = agent.classify_intent(None or "")

    assert result in INTENT_LABELS


# route — happy path: known intent returns agent list
def test_route_known_intent(agent):
    result = agent.route("MENTOR", {})

    assert len(result) > 0

    assert "mentor_agent" in result[0]


# route — edge case: UNKNOWN intent returns empty list
def test_route_unknown_intent(agent):
    result = agent.route("UNKNOWN", {})

    assert result == []


# route — failure: completely invalid intent string
def test_route_invalid_intent(agent):
    result = agent.route("GARBAGE_INTENT", {})

    assert result == []


# run — happy path: returns dict with required keys
def test_run_returns_required_keys(agent):
    result = agent.run("what is a binary tree", {"session_id": "s1"})

    assert "intent" in result

    assert "agents" in result

    assert "response" in result


# run — edge case: empty text still returns valid dict
def test_run_empty_text(agent):
    result = agent.run("", {})

    assert isinstance(result, dict)


# AGENT_REGISTRY — all values are valid module paths
def test_agent_registry_values_are_strings():
    for key, val in AGENT_REGISTRY.items():
        assert isinstance(val, str)

        assert val.startswith("agents.")
