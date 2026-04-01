# calendar_mcp.py — Google Calendar MCP wrapper

import os

import httpx

from dotenv import load_dotenv

load_dotenv()

CALENDAR_BASE = "https://www.googleapis.com/calendar/v3"


class CalendarMCP:

    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")

        self._token = os.getenv("GOOGLE_ACCESS_TOKEN", "")

        self._headers = {"Authorization": f"Bearer {self._token}"}

    def create(self, title: str, start: str, end: str) -> dict:
        # POST event to primary calendar, returns event dict
        body = {"summary": title, "start": {"dateTime": start}, "end": {"dateTime": end}}

        try:
            r = httpx.post(f"{CALENDAR_BASE}/calendars/primary/events", json=body, headers=self._headers)

            return r.json() if r.status_code == 200 else {"error": r.status_code, "title": title}

        except Exception:
            return {"error": "request_failed", "title": title}

    def list(self, date: str) -> list[dict]:
        # GET events for a specific date from primary calendar
        params = {"timeMin": f"{date}T00:00:00Z", "timeMax": f"{date}T23:59:59Z", "singleEvents": True}

        try:
            r = httpx.get(f"{CALENDAR_BASE}/calendars/primary/events", params=params, headers=self._headers)

            return r.json().get("items", []) if r.status_code == 200 else []

        except Exception:
            return []

    def delete(self, event_id: str) -> bool:
        # DELETE event from primary calendar
        try:
            r = httpx.delete(f"{CALENDAR_BASE}/calendars/primary/events/{event_id}", headers=self._headers)

            return r.status_code == 204

        except Exception:
            return False
