# test_task_agent.py — unit tests for TaskAgent with mocked MCP calls

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def agent():
    with patch("mcp.calendar_mcp.httpx.post") as _:
        with patch("mcp.calendar_mcp.httpx.get") as _:
            with patch("mcp.github_mcp.httpx.get") as _:
                from agents.task_agent import TaskAgent
                a = TaskAgent()
                return a


# create_event — happy path: returns dict with title
def test_create_event_happy(agent):
    with patch.object(agent._calendar, "create", return_value={"id": "evt1", "title": "Standup"}):
        result = agent.create_event("Standup", "2025-01-01T09:00:00Z", "2025-01-01T09:30:00Z")
        assert result["title"] == "Standup"


# create_event — failure: MCP error returns error dict
def test_create_event_mcp_failure(agent):
    with patch.object(agent._calendar, "create", return_value={"error": 401, "title": "X"}):
        result = agent.create_event("X", "", "")
        assert "error" in result


# list_events — happy path: returns list
def test_list_events_returns_list(agent):
    with patch.object(agent._calendar, "list", return_value=[{"id": "e1"}]):
        result = agent.list_events("2025-01-01")
        assert isinstance(result, list)


# list_events — edge case: no events returns empty list
def test_list_events_empty(agent):
    with patch.object(agent._calendar, "list", return_value=[]):
        result = agent.list_events("2025-01-01")
        assert result == []


# delete_event — happy path: returns ok True
def test_delete_event_success(agent):
    with patch.object(agent._calendar, "delete", return_value=True):
        result = agent.delete_event("evt-123")
        assert result["ok"] is True
        assert result["deleted"] == "evt-123"


# delete_event — failure: MCP returns False
def test_delete_event_failure(agent):
    with patch.object(agent._calendar, "delete", return_value=False):
        result = agent.delete_event("evt-999")
        assert result["ok"] is False


# get_pr_status — happy path: returns state field
def test_get_pr_status_happy(agent):
    with patch.object(agent._github, "get_pr_status", return_value={"repo": "orbit", "pr": 1, "state": "open"}):
        result = agent.get_pr_status("orbit", 1)
        assert result["state"] == "open"


# list_open_prs — returns list
def test_list_open_prs_returns_list(agent):
    with patch.object(agent._github, "list_open_prs", return_value=[{"number": 1, "title": "fix bug"}]):
        result = agent.list_open_prs("orbit")
        assert len(result) == 1


# run — default action is list_events
def test_run_default_list_events(agent):
    with patch.object(agent, "list_events", return_value=[]):
        result = agent.run("CALENDAR", {})
        assert "events" in result


# run — create action dispatches correctly
def test_run_create_action(agent):
    with patch.object(agent, "create_event", return_value={"id": "e1", "title": "T"}):
        result = agent.run("CALENDAR", {"action": "create", "title": "T", "start": "", "end": ""})
        assert "id" in result
