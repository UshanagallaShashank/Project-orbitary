# eval — mentor agent format correctness

import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agents.mentor_agent import MENTOR_PARTS

EVAL_FILE = Path("evals/mentor_agent/eval_results.jsonl")

TOPICS = ["binary search", "recursion", "dynamic programming"]


@pytest.fixture(scope="module")
def agent():
    with patch("agents.mentor_agent.MentorAgent._build_client", return_value=MagicMock()):
        from agents.mentor_agent import MentorAgent
        return MentorAgent()


def write_result(topic: str, has_all_parts: bool, latency_ms: int):
    EVAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    row = {"topic": topic, "all_parts_present": has_all_parts, "latency_ms": latency_ms}
    with open(EVAL_FILE, "a") as f:
        f.write(json.dumps(row) + "\n")


def test_mentor_eval_format(agent):
    # Verifies 10-part JSON format is returned for all eval topics
    for topic in TOPICS:
        mock_data = {p: f"content for {p}" for p in MENTOR_PARTS}
        agent._client.models.generate_content.return_value = MagicMock(
            text=json.dumps(mock_data)
        )
        start = time.monotonic()
        result = agent.teach(topic)
        latency_ms = int((time.monotonic() - start) * 1000)
        has_all = result["response"] is not None and set(result["response"].keys()) == set(MENTOR_PARTS)
        write_result(topic, has_all, latency_ms)
        assert has_all, f"Missing parts for topic: {topic}"
