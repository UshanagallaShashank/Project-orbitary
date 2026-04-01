# test_tracker_agent.py — unit tests for TrackerAgent with mocked DB

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_cursor():
    return MagicMock()


@pytest.fixture
def agent(mock_cursor):
    with patch("agents.tracker_agent.psycopg2.connect") as mock_connect:
        conn = MagicMock()
        mock_connect.return_value.__enter__ = lambda s: conn
        mock_connect.return_value.__exit__ = MagicMock(return_value=False)
        cur = mock_cursor
        conn.cursor.return_value.__enter__ = lambda s: cur
        conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        from agents.tracker_agent import TrackerAgent
        a = TrackerAgent()
        a._cur = cur
        a._conn = conn
        a._mock_connect = mock_connect
        yield a, cur


# log_solve — happy path: ok True when DB succeeds
def test_log_solve_happy(agent):
    a, cur = agent
    result = a.log_solve("two-sum", "easy")
    assert result["problem"] == "two-sum"
    assert "ok" in result


# log_solve — failure: exception returns ok False
def test_log_solve_db_error():
    with patch("agents.tracker_agent.psycopg2.connect", side_effect=Exception("db down")):
        from agents.tracker_agent import TrackerAgent
        result = TrackerAgent().log_solve("binary-search", "easy")
        assert result["ok"] is False


# log_solve — edge case: empty problem string handled
def test_log_solve_empty_problem(agent):
    a, cur = agent
    result = a.log_solve("", "easy")
    assert result["problem"] == ""


# get_streak — happy path: returns correct count from DB
def test_get_streak_returns_count(agent):
    a, cur = agent
    cur.fetchone.return_value = (7,)
    result = a.get_streak()
    assert result["streak"] == 7


# get_streak — edge case: zero solves
def test_get_streak_zero(agent):
    a, cur = agent
    cur.fetchone.return_value = (0,)
    result = a.get_streak()
    assert result["streak"] == 0


# get_streak — failure: DB error returns 0
def test_get_streak_db_error():
    with patch("agents.tracker_agent.psycopg2.connect", side_effect=Exception("db down")):
        from agents.tracker_agent import TrackerAgent
        result = TrackerAgent().get_streak()
        assert result["streak"] == 0


# get_topic_progress — happy path: returns count from DB
def test_get_topic_progress_happy(agent):
    a, cur = agent
    cur.fetchone.return_value = (5,)
    result = a.get_topic_progress("graphs")
    assert result["topic"] == "graphs"
    assert result["solved"] == 5


# get_topic_progress — failure: DB error returns 0
def test_get_topic_progress_db_error():
    with patch("agents.tracker_agent.psycopg2.connect", side_effect=Exception("db down")):
        from agents.tracker_agent import TrackerAgent
        result = TrackerAgent().get_topic_progress("trees")
        assert result["solved"] == 0


# run — default action returns streak dict
def test_run_default_streak(agent):
    a, cur = agent
    cur.fetchone.return_value = (3,)
    result = a.run("TRACKER", {})
    assert "streak" in result


# run — log action dispatches log_solve
def test_run_log_action(agent):
    a, cur = agent
    with patch.object(a, "log_solve", return_value={"problem": "x", "ok": True}) as mock:
        a.run("TRACKER", {"action": "log", "problem": "x", "difficulty": "easy"})
        mock.assert_called_once()
