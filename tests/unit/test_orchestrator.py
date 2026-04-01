# test_orchestrator.py — unit tests for OrchestratorAgent

import pytest
from unittest.mock import MagicMock, patch

from agents.orchestrator import AGENT_REGISTRY, INTENT_LABELS


@pytest.fixture
def agent():
    with patch("agents.orchestrator.OrchestratorAgent._build_client", return_value=MagicMock()):
        from agents.orchestrator import OrchestratorAgent
        return OrchestratorAgent()


# classify_intent — happy path: Gemini returns valid label
def test_classify_intent_valid_label(agent):
    agent._client.models.generate_content.return_value = MagicMock(text="MENTOR")
    result = agent.classify_intent("explain recursion")
    assert result == "MENTOR"


# classify_intent — edge case: Gemini returns junk → UNKNOWN
def test_classify_intent_bad_response(agent):
    agent._client.models.generate_content.return_value = MagicMock(text="JUNK")
    result = agent.classify_intent("blah blah")
    assert result == "UNKNOWN"


# classify_intent — failure: empty string → UNKNOWN without calling Gemini
def test_classify_intent_empty_text(agent):
    result = agent.classify_intent("")
    agent._client.models.generate_content.assert_not_called()
    assert result == "UNKNOWN"


# classify_intent — failure: Gemini throws → UNKNOWN
def test_classify_intent_exception(agent):
    agent._client.models.generate_content.side_effect = Exception("timeout")
    result = agent.classify_intent("what is a heap")
    assert result == "UNKNOWN"


# route — happy path: every registry intent maps to one agent
def test_route_all_known_intents(agent):
    for intent in AGENT_REGISTRY:
        result = agent.route(intent, {})
        assert len(result) == 1
        assert result[0].startswith("agents.")


# route — edge case: UNKNOWN returns empty list
def test_route_unknown_returns_empty(agent):
    assert agent.route("UNKNOWN", {}) == []


# route — failure: garbage intent returns empty list
def test_route_garbage_intent(agent):
    assert agent.route("BLASTOFF", {}) == []


# run — happy path: returns all required keys
def test_run_returns_required_keys(agent):
    agent._client.models.generate_content.return_value = MagicMock(text="DSA")
    result = agent.run("explain binary search", {"session_id": "s1"})
    assert set(result.keys()) >= {"intent", "agents", "response"}


# run — intent value is one of INTENT_LABELS
def test_run_intent_is_valid_label(agent):
    agent._client.models.generate_content.return_value = MagicMock(text="TRACKER")
    result = agent.run("show my leetcode streak", {})
    assert result["intent"] in INTENT_LABELS


# AGENT_REGISTRY values are all valid module paths
def test_registry_module_paths():
    for val in AGENT_REGISTRY.values():
        assert val.startswith("agents.")
