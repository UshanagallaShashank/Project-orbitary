# TaskAgent — handles Calendar events and GitHub status via MCP

import os

from dotenv import load_dotenv

load_dotenv()


class TaskAgent:

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN", "")

    def create_event(self, title: str, start: str, end: str) -> dict:
        # Stub — replaced in F6 with real Calendar MCP call
        return {"status": "stub", "event": title}

    def list_events(self, date: str) -> list[dict]:
        # Stub — returns empty list until F6
        return []

    def delete_event(self, event_id: str) -> dict:
        # Stub — replaced in F6
        return {"status": "stub", "deleted": event_id}

    def run(self, intent: str, context: dict) -> dict:
        # Dispatch based on intent sub-action
        action = context.get("action", "list")

        if action == "create":
            return self.create_event(
                context.get("title", ""),
                context.get("start", ""),
                context.get("end", ""),
            )

        return {"events": self.list_events(context.get("date", ""))}
