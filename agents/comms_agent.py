# comms_agent.py — reads and sends Gmail, reads Calendar via MCP

import os

from mcp.gmail_mcp import GmailMCP

from mcp.calendar_mcp import CalendarMCP

from dotenv import load_dotenv

load_dotenv()


class CommsAgent:

    def __init__(self):
        self._gmail = GmailMCP()

        self._calendar = CalendarMCP()

    def list_emails(self, count: int = 5) -> list[dict]:
        # Returns last N emails via Gmail MCP
        return self._gmail.list(count)

    def send_email(self, to: str, subject: str, body: str) -> dict:
        # Sends email via Gmail MCP
        return self._gmail.send(to, subject, body)

    def read_email(self, email_id: str) -> dict:
        # Reads full email body via Gmail MCP
        return self._gmail.read(email_id)

    def list_calendar_events(self, date: str) -> list[dict]:
        # Lists calendar events for a date via Calendar MCP
        return self._calendar.list(date)

    def run(self, intent: str, context: dict) -> dict:
        # Dispatches based on action key
        action = context.get("action", "list_emails")

        if action == "send_email":
            return self.send_email(context.get("to", ""), context.get("subject", ""), context.get("body", ""))

        if action == "read_email":
            return self.read_email(context.get("email_id", ""))

        if action == "list_calendar":
            return {"events": self.list_calendar_events(context.get("date", ""))}

        return {"emails": self.list_emails(context.get("count", 5))}
