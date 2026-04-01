# TrackerAgent — LeetCode solves, DSA streaks, topic progress

import os

from dotenv import load_dotenv

load_dotenv()

LEETCODE_API = "https://leetcode.com/graphql"


class TrackerAgent:

    def __init__(self):
        self.username = os.getenv("GITHUB_USERNAME", "")

    def log_solve(self, problem: str, difficulty: str) -> dict:
        # Stub — writes to PostgreSQL in F7
        return {"status": "stub", "problem": problem, "difficulty": difficulty}

    def get_streak(self) -> dict:
        # Stub — reads streak from PostgreSQL in F7
        return {"streak": 0, "last_solve": None}

    def get_topic_progress(self, topic: str) -> dict:
        # Stub — returns topic solve counts in F7
        return {"topic": topic, "solved": 0, "total": 0}

    def run(self, intent: str, context: dict) -> dict:
        # Dispatch based on sub-action
        action = context.get("action", "streak")

        if action == "log":
            return self.log_solve(context.get("problem", ""), context.get("difficulty", ""))

        if action == "topic":
            return self.get_topic_progress(context.get("topic", ""))

        return self.get_streak()
