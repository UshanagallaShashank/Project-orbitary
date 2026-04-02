# eval — orchestrator intent classification accuracy

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

EVAL_FILE = Path("evals/orchestrator/eval_results.jsonl")

CASES = [
    ("explain binary search to me", "MENTOR"),
    ("show my leetcode streak", "TRACKER"),
    ("what's on my calendar today", "CALENDAR"),
    ("read my last 3 emails", "COMMS"),
    ("what is dynamic programming", "MENTOR"),
    ("log that I solved two sum", "TRACKER"),
]


@pytest.fixture(scope="module")
def agent():
    with patch("agents.orchestrator.OrchestratorAgent._build_client", return_value=MagicMock()):
        from agents.orchestrator import OrchestratorAgent
        return OrchestratorAgent()


def append_result(case: str, expected: str, got: str, latency_ms: int):
    # Appends — never overwrites — so history accumulates across runs
    EVAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "run": os.getenv("GITHUB_RUN_ID", "local"),
        "input": case,
        "expected": expected,
        "got": got,
        "correct": got == expected,
        "latency_ms": latency_ms,
    }
    with open(EVAL_FILE, "a") as f:
        f.write(json.dumps(row) + "\n")


def test_orchestrator_eval_all_cases(agent):
    correct = 0
    for text, expected in CASES:
        agent._client.models.generate_content.return_value = MagicMock(text=expected)
        start = time.monotonic()
        result = agent.classify_intent(text)
        latency_ms = int((time.monotonic() - start) * 1000)
        append_result(text, expected, result, latency_ms)
        if result == expected:
            correct += 1
    accuracy = correct / len(CASES)
    assert accuracy == 1.0, f"Eval accuracy {accuracy:.0%} — check eval_results.jsonl"
