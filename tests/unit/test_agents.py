# test_agents.py — unit tests for TaskAgent, TrackerAgent, CommsAgent, MentorAgent

import pytest

from agents.task_agent import TaskAgent
from agents.tracker_agent import TrackerAgent
from agents.comms_agent import CommsAgent
from agents.mentor_agent import MentorAgent, MENTOR_PARTS


# --- TaskAgent ---

def test_task_create_event_stub():
    agent = TaskAgent()
    result = agent.create_event("Standup", "2025-01-01T09:00", "2025-01-01T09:30")
    assert result["status"] == "stub"
    assert result["event"] == "Standup"


def test_task_list_events_returns_list():
    result = TaskAgent().list_events("2025-01-01")
    assert isinstance(result, list)


def test_task_delete_event_stub():
    result = TaskAgent().delete_event("evt-123")
    assert result["deleted"] == "evt-123"


def test_task_run_defaults_to_list():
    result = TaskAgent().run("CALENDAR", {})
    assert "events" in result


# --- TrackerAgent ---

def test_tracker_log_solve_stub():
    result = TrackerAgent().log_solve("two-sum", "easy")
    assert result["problem"] == "two-sum"


def test_tracker_get_streak_stub():
    result = TrackerAgent().get_streak()
    assert "streak" in result
    assert result["streak"] == 0


def test_tracker_topic_progress_stub():
    result = TrackerAgent().get_topic_progress("graphs")
    assert result["topic"] == "graphs"


# --- CommsAgent ---

def test_comms_list_emails_returns_list():
    result = CommsAgent().list_emails()
    assert isinstance(result, list)


def test_comms_send_email_stub():
    result = CommsAgent().send_email("a@b.com", "hi", "body")
    assert result["to"] == "a@b.com"


def test_comms_list_calendar_returns_list():
    result = CommsAgent().list_calendar_events("2025-01-01")
    assert isinstance(result, list)


# --- MentorAgent ---

def test_mentor_parts_count():
    assert len(MENTOR_PARTS) == 10


def test_mentor_build_prompt_contains_topic():
    agent = MentorAgent()
    prompt = agent.build_prompt("recursion")
    assert "recursion" in prompt


def test_mentor_run_returns_format():
    result = MentorAgent().run("recursion", {})
    assert result["format"] == MENTOR_PARTS
    assert result["topic"] == "recursion"
