# gmail_mcp.py — Gmail MCP wrapper

import os

from dotenv import load_dotenv

load_dotenv()


class GmailMCP:

    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")

    def list(self, count: int = 5) -> list[dict]:
        # Stub — replaced in F9
        return []

    def send(self, to: str, subject: str, body: str) -> dict:
        # Stub — replaced in F9
        return {"status": "stub"}

    def read(self, email_id: str) -> dict:
        # Stub — replaced in F9
        return {"id": email_id, "body": None}
