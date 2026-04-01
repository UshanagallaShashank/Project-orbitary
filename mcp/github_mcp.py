# github_mcp.py — GitHub MCP wrapper for PR and check status

import os

import httpx

from dotenv import load_dotenv

load_dotenv()

GH_BASE = "https://api.github.com"


class GithubMCP:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")

        self.username = os.getenv("GITHUB_USERNAME", "")

        self._headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json"}

    def get_pr_status(self, repo: str, pr_number: int) -> dict:
        # Returns PR title, state, and merge status
        try:
            r = httpx.get(f"{GH_BASE}/repos/{self.username}/{repo}/pulls/{pr_number}", headers=self._headers)

            data = r.json()

            return {"repo": repo, "pr": pr_number, "state": data.get("state"), "merged": data.get("merged", False)}

        except Exception:
            return {"repo": repo, "pr": pr_number, "state": None}

    def list_open_prs(self, repo: str) -> list[dict]:
        # Returns list of open PR numbers and titles
        try:
            r = httpx.get(f"{GH_BASE}/repos/{self.username}/{repo}/pulls?state=open", headers=self._headers)

            return [{"number": p["number"], "title": p["title"]} for p in r.json()]

        except Exception:
            return []

    def get_check_runs(self, repo: str, commit_sha: str) -> list[dict]:
        # Returns CI check statuses for a commit
        try:
            r = httpx.get(f"{GH_BASE}/repos/{self.username}/{repo}/commits/{commit_sha}/check-runs", headers=self._headers)

            return [{"name": c["name"], "status": c["status"]} for c in r.json().get("check_runs", [])]

        except Exception:
            return []
