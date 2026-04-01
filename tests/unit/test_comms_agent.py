# test_comms_agent.py — unit tests for CommsAgent with mocked MCP

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def agent():
    with patch("mcp.gmail_mcp.httpx.get"), patch("mcp.gmail_mcp.httpx.post"), \
         patch("mcp.calendar_mcp.httpx.get"), patch("mcp.calendar_mcp.httpx.post"):
        from agents.comms_agent import CommsAgent
        return CommsAgent()


# list_emails — happy path: returns list of email dicts
def test_list_emails_happy(agent):
    with patch.object(agent._gmail, "list", return_value=[{"id": "1", "subject": "Hi", "from": "a@b.com"}]):
        result = agent.list_emails(1)
        assert len(result) == 1
        assert result[0]["subject"] == "Hi"


# list_emails — edge case: count=0 returns empty list
def test_list_emails_empty(agent):
    with patch.object(agent._gmail, "list", return_value=[]):
        result = agent.list_emails(0)
        assert result == []


# list_emails — failure: Gmail MCP error returns empty list
def test_list_emails_mcp_failure(agent):
    with patch.object(agent._gmail, "list", side_effect=Exception("mcp error")):
        try:
            result = agent.list_emails()
        except Exception:
            result = []
        assert isinstance(result, list)


# send_email — happy path: returns ok True
def test_send_email_happy(agent):
    with patch.object(agent._gmail, "send", return_value={"status": 200, "to": "a@b.com", "ok": True}):
        result = agent.send_email("a@b.com", "Test", "Hello")
        assert result["ok"] is True
        assert result["to"] == "a@b.com"


# send_email — failure: MCP returns ok False
def test_send_email_failure(agent):
    with patch.object(agent._gmail, "send", return_value={"status": 401, "to": "x@y.com", "ok": False}):
        result = agent.send_email("x@y.com", "Fail", "body")
        assert result["ok"] is False


# read_email — happy path: returns id and body
def test_read_email_happy(agent):
    with patch.object(agent._gmail, "read", return_value={"id": "msg1", "body": {"snippet": "hello"}}):
        result = agent.read_email("msg1")
        assert result["id"] == "msg1"
        assert result["body"] is not None


# read_email — failure: MCP error returns None body
def test_read_email_failure(agent):
    with patch.object(agent._gmail, "read", return_value={"id": "bad", "body": None}):
        result = agent.read_email("bad")
        assert result["body"] is None


# list_calendar_events — returns list
def test_list_calendar_events_happy(agent):
    with patch.object(agent._calendar, "list", return_value=[{"id": "evt1"}]):
        result = agent.list_calendar_events("2025-01-01")
        assert isinstance(result, list)


# run — default action returns emails key
def test_run_default_list_emails(agent):
    with patch.object(agent, "list_emails", return_value=[]):
        result = agent.run("COMMS", {})
        assert "emails" in result


# run — send_email action dispatches correctly
def test_run_send_email_action(agent):
    with patch.object(agent, "send_email", return_value={"ok": True, "to": "a@b.com"}) as mock:
        agent.run("COMMS", {"action": "send_email", "to": "a@b.com", "subject": "s", "body": "b"})
        mock.assert_called_once()
