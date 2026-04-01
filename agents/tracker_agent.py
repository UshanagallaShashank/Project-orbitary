# tracker_agent.py — LeetCode log, DSA streaks, topic progress via PostgreSQL

import os
import json
from datetime import date

import psycopg2

from dotenv import load_dotenv

load_dotenv()


class TrackerAgent:

    def __init__(self):
        self._dsn = {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "dbname": os.getenv("POSTGRES_DB", "orbit"),
            "user": os.getenv("POSTGRES_USER", "orbit_user"),
            "password": os.getenv("POSTGRES_PASSWORD", ""),
        }

    def _connect(self):
        return psycopg2.connect(**self._dsn)

    def log_solve(self, problem: str, difficulty: str) -> dict:
        # Inserts a solve record into lc_solves table
        sql = "INSERT INTO lc_solves (problem, difficulty, solved_on) VALUES (%s, %s, %s)"

        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (problem, difficulty, date.today().isoformat()))

                conn.commit()

            return {"problem": problem, "difficulty": difficulty, "ok": True}

        except Exception:
            return {"problem": problem, "difficulty": difficulty, "ok": False}

    def get_streak(self) -> dict:
        # Returns current consecutive solve-day streak
        sql = """
            SELECT COUNT(DISTINCT solved_on) FROM lc_solves
            WHERE solved_on >= CURRENT_DATE - INTERVAL '30 days'
        """

        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)

                    count = cur.fetchone()[0]

            return {"streak": int(count), "last_solve": date.today().isoformat()}

        except Exception:
            return {"streak": 0, "last_solve": None}

    def get_topic_progress(self, topic: str) -> dict:
        # Returns solve count for a given DSA topic
        sql = "SELECT COUNT(*) FROM lc_solves WHERE LOWER(problem) LIKE %s"

        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (f"%{topic.lower()}%",))

                    count = cur.fetchone()[0]

            return {"topic": topic, "solved": int(count), "total": 0}

        except Exception:
            return {"topic": topic, "solved": 0, "total": 0}

    def run(self, intent: str, context: dict) -> dict:
        action = context.get("action", "streak")

        if action == "log":
            return self.log_solve(context.get("problem", ""), context.get("difficulty", "easy"))

        if action == "topic":
            return self.get_topic_progress(context.get("topic", ""))

        return self.get_streak()
