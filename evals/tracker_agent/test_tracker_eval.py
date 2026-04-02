# eval — tracker agent data shape correctness

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

EVAL_FILE = Path("evals/tracker_agent/eval_results.jsonl")


def append_result(action: str, passed: bool, latency_ms: int):
    EVAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "run": os.getenv("GITHUB_RUN_ID", "local"),
        "action": action,
        "passed": passed,
        "latency_ms": latency_ms,
    }
    with open(EVAL_FILE, "a") as f:
        f.write(json.dumps(row) + "\n")


def test_tracker_eval_streak_shape():
    with patch("agents.tracker_agent.psycopg2.connect", side_effect=Exception("no db")):
        from agents.tracker_agent import TrackerAgent
        start = time.monotonic()
        result = TrackerAgent().get_streak()
        latency_ms = int((time.monotonic() - start) * 1000)
        passed = "streak" in result and "last_solve" in result
        append_result("get_streak", passed, latency_ms)
        assert passed


def test_tracker_eval_log_shape():
    with patch("agents.tracker_agent.psycopg2.connect", side_effect=Exception("no db")):
        from agents.tracker_agent import TrackerAgent
        start = time.monotonic()
        result = TrackerAgent().log_solve("two-sum", "easy")
        latency_ms = int((time.monotonic() - start) * 1000)
        passed = "problem" in result and "ok" in result
        append_result("log_solve", passed, latency_ms)
        assert passed


def test_tracker_eval_topic_shape():
    with patch("agents.tracker_agent.psycopg2.connect", side_effect=Exception("no db")):
        from agents.tracker_agent import TrackerAgent
        start = time.monotonic()
        result = TrackerAgent().get_topic_progress("graphs")
        latency_ms = int((time.monotonic() - start) * 1000)
        passed = "topic" in result and "solved" in result
        append_result("get_topic_progress", passed, latency_ms)
        assert passed
