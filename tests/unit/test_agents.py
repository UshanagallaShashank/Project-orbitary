# test_agents.py — unit tests for TrackerAgent, CommsAgent, MentorAgent

import pytest
from unittest.mock import MagicMock, patch

from agents.tracker_agent import TrackerAgent
from agents.comms_agent import CommsAgent
from agents.mentor_agent import MentorAgent, MENTOR_PARTS


# --- TrackerAgent ---

def test_tracker_log_solve_returns_problem():
    result = TrackerAgent().log_solve("two-sum", "easy")
    assert result["problem"] == "two-sum"


def test_tracker_get_streak_returns_dict():
    result = TrackerAgent().get_streak()
    assert "streak" in result


def test_tracker_topic_progress_returns_topic():
    result = TrackerAgent().get_topic_progress("graphs")
    assert result["topic"] == "graphs"


def test_tracker_run_defaults_to_streak():
    result = TrackerAgent().run("TRACKER", {})
    assert "streak" in result


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
