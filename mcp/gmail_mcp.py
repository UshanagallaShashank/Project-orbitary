# gmail_mcp.py — Gmail MCP wrapper using Google API

import os

import httpx

from dotenv import load_dotenv

load_dotenv()

GMAIL_BASE = "https://gmail.googleapis.com/gmail/v1/users/me"


class GmailMCP:

    def __init__(self):
        self._token = os.getenv("GOOGLE_ACCESS_TOKEN", "")

        self._headers = {"Authorization": f"Bearer {self._token}"}

    def list(self, count: int = 5) -> list[dict]:
        # Returns last N email subjects and sender names
        try:
            r = httpx.get(f"{GMAIL_BASE}/messages?maxResults={count}", headers=self._headers)

            messages = r.json().get("messages", [])

            results = []

            for m in messages[:count]:
                detail = httpx.get(f"{GMAIL_BASE}/messages/{m['id']}?format=metadata", headers=self._headers)

                headers = {h["name"]: h["value"] for h in detail.json().get("payload", {}).get("headers", [])}

                results.append({"id": m["id"], "subject": headers.get("Subject", ""), "from": headers.get("From", "")})

            return results

        except Exception:
            return []

    def send(self, to: str, subject: str, body: str) -> dict:
        # Sends an email via Gmail API using RFC 2822 format
        import base64

        raw = f"To: {to}\r\nSubject: {subject}\r\n\r\n{body}"

        encoded = base64.urlsafe_b64encode(raw.encode()).decode()

        try:
            r = httpx.post(f"{GMAIL_BASE}/messages/send", json={"raw": encoded}, headers=self._headers)

            return {"status": r.status_code, "to": to, "ok": r.status_code == 200}

        except Exception:
            return {"status": 0, "to": to, "ok": False}

    def read(self, email_id: str) -> dict:
        # Returns full email body for a given message ID
        try:
            r = httpx.get(f"{GMAIL_BASE}/messages/{email_id}?format=full", headers=self._headers)

            return {"id": email_id, "body": r.json()}

        except Exception:
            return {"id": email_id, "body": None}
