# CommsAgent — reads and sends Gmail, reads Calendar via MCP

import os

from dotenv import load_dotenv

load_dotenv()


class CommsAgent:

    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")

    def list_emails(self, count: int = 5) -> list[dict]:
        # Stub — replaced in F9 with Gmail MCP call
        return []

    def send_email(self, to: str, subject: str, body: str) -> dict:
        # Stub — replaced in F9
        return {"status": "stub", "to": to}

    def list_calendar_events(self, date: str) -> list[dict]:
        # Stub — replaced in F9 with Calendar MCP call
        return []

    def run(self, intent: str, context: dict) -> dict:
        # Dispatch based on sub-action
        action = context.get("action", "list_emails")

        if action == "send_email":
            return self.send_email(
                context.get("to", ""),
                context.get("subject", ""),
                context.get("body", ""),
            )

        if action == "list_calendar":
            return {"events": self.list_calendar_events(context.get("date", ""))}

        return {"emails": self.list_emails(context.get("count", 5))}
