# github_mcp.py — GitHub MCP wrapper for PR and check status

import os

from dotenv import load_dotenv

load_dotenv()


class GithubMCP:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN", "")

        self.username = os.getenv("GITHUB_USERNAME", "")

    def get_pr_status(self, repo: str, pr_number: int) -> dict:
        # Stub — replaced in F6
        return {"repo": repo, "pr": pr_number, "status": None}

    def list_open_prs(self, repo: str) -> list[dict]:
        # Stub — replaced in F6
        return []

    def get_check_runs(self, repo: str, commit_sha: str) -> list[dict]:
        # Stub — replaced in F6
        return []
