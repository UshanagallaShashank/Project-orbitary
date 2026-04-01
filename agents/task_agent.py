# task_agent.py — Google Calendar events + GitHub PR status via MCP

import os

from mcp.calendar_mcp import CalendarMCP

from mcp.github_mcp import GithubMCP

from dotenv import load_dotenv

load_dotenv()


class TaskAgent:

    def __init__(self):
        self._calendar = CalendarMCP()

        self._github = GithubMCP()

    def create_event(self, title: str, start: str, end: str) -> dict:
        # Creates a Calendar event via MCP
        return self._calendar.create(title, start, end)

    def list_events(self, date: str) -> list[dict]:
        # Lists Calendar events for a given date via MCP
        return self._calendar.list(date)

    def delete_event(self, event_id: str) -> dict:
        # Deletes a Calendar event by ID
        deleted = self._calendar.delete(event_id)

        return {"deleted": event_id, "ok": deleted}

    def get_pr_status(self, repo: str, pr_number: int) -> dict:
        # Returns PR status from GitHub MCP
        return self._github.get_pr_status(repo, pr_number)

    def list_open_prs(self, repo: str) -> list[dict]:
        # Returns open PRs for a repo
        return self._github.list_open_prs(repo)

    def run(self, intent: str, context: dict) -> dict:
        # Dispatches based on action key in context
        action = context.get("action", "list_events")

        if action == "create":
            return self.create_event(context.get("title", ""), context.get("start", ""), context.get("end", ""))

        if action == "delete":
            return self.delete_event(context.get("event_id", ""))

        if action == "pr_status":
            return self.get_pr_status(context.get("repo", ""), context.get("pr_number", 0))

        if action == "list_prs":
            return {"prs": self.list_open_prs(context.get("repo", ""))}

        return {"events": self.list_events(context.get("date", ""))}
