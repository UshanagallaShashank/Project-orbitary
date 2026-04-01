# calendar_mcp.py — Google Calendar MCP wrapper

import os

from dotenv import load_dotenv

load_dotenv()


class CalendarMCP:

    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")

    def create(self, title: str, start: str, end: str) -> dict:
        # Stub — replaced in F6
        return {"id": None, "title": title}

    def list(self, date: str) -> list[dict]:
        # Stub — replaced in F6
        return []

    def delete(self, event_id: str) -> bool:
        # Stub — replaced in F6
        return False
