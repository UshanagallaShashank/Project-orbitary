# test_mentor_agent.py — unit tests for MentorAgent with mocked Gemini

import json
import pytest
from unittest.mock import MagicMock, patch

from agents.mentor_agent import MENTOR_PARTS


@pytest.fixture
def agent():
    with patch("agents.mentor_agent.MentorAgent._build_client", return_value=MagicMock()):
        from agents.mentor_agent import MentorAgent
        return MentorAgent()


def _mock_response(agent, data: dict):
    agent._client.models.generate_content.return_value = MagicMock(text=json.dumps(data))


# MENTOR_PARTS — exactly 10 parts in correct order
def test_mentor_parts_count():
    assert len(MENTOR_PARTS) == 10


def test_mentor_parts_first_is_simple_explanation():
    assert MENTOR_PARTS[0] == "simple_explanation"


def test_mentor_parts_last_is_quick_summary():
    assert MENTOR_PARTS[-1] == "quick_summary"


# build_prompt — contains topic and all 10 part names
def test_build_prompt_contains_topic(agent):
    prompt = agent.build_prompt("binary search")
    assert "binary search" in prompt


def test_build_prompt_contains_all_parts(agent):
    prompt = agent.build_prompt("recursion")
    for part in MENTOR_PARTS:
        assert part in prompt


# teach — happy path: returns parsed response with all 10 keys
def test_teach_happy_path(agent):
    data = {p: f"content for {p}" for p in MENTOR_PARTS}
    _mock_response(agent, data)
    result = agent.teach("binary search")
    assert result["topic"] == "binary search"
    assert result["response"] is not None
    assert set(result["response"].keys()) == set(MENTOR_PARTS)


# teach — edge case: Gemini returns invalid JSON falls back to None
def test_teach_invalid_json(agent):
    agent._client.models.generate_content.return_value = MagicMock(text="not valid json {{")
    result = agent.teach("graphs")
    assert result["response"] is None


# teach — failure: Gemini throws returns None response
def test_teach_gemini_exception(agent):
    agent._client.models.generate_content.side_effect = Exception("timeout")
    result = agent.teach("heaps")
    assert result["response"] is None


# teach — no client: returns None response without crashing
def test_teach_no_client():
    with patch("agents.mentor_agent.MentorAgent._build_client", return_value=None):
        from agents.mentor_agent import MentorAgent
        result = MentorAgent().teach("trees")
        assert result["response"] is None


# run — returns same shape as teach
def test_run_returns_teach_shape(agent):
    data = {p: "x" for p in MENTOR_PARTS}
    _mock_response(agent, data)
    result = agent.run("sorting", {})
    assert "topic" in result
    assert "format" in result
    assert "response" in result


# run — format field always equals MENTOR_PARTS
def test_run_format_equals_mentor_parts(agent):
    data = {p: "x" for p in MENTOR_PARTS}
    _mock_response(agent, data)
    result = agent.run("graphs", {})
    assert result["format"] == MENTOR_PARTS
