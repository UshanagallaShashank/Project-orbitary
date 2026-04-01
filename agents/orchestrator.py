# orchestrator.py — master router, classifies intent, fans out to agents

import os
from unittest.mock import MagicMock

from dotenv import load_dotenv

load_dotenv()

INTENT_LABELS = ["DSA", "CALENDAR", "MENTOR", "TRACKER", "MEMORY", "COMMS", "UNKNOWN"]

AGENT_REGISTRY = {
    "DSA": "agents.tracker_agent",
    "CALENDAR": "agents.task_agent",
    "MENTOR": "agents.mentor_agent",
    "TRACKER": "agents.tracker_agent",
    "MEMORY": "agents.memory_agent",
    "COMMS": "agents.comms_agent",
}

_CLASSIFY_PROMPT = (
    f"Classify the intent of this message as exactly one of: {', '.join(INTENT_LABELS)}. "
    "Reply with only the label, nothing else."
)


class OrchestratorAgent:

    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

        self._client = self._build_client()

    def _build_client(self):
        # Returns real genai client if key present, else a safe no-op mock
        api_key = os.getenv("GEMINI_API_KEY", "")

        if not api_key:
            return None

        from google import genai

        return genai.Client(api_key=api_key)

    def classify_intent(self, text: str) -> str:
        # Calls Gemini 2.5 to classify intent into one of INTENT_LABELS
        if not text or not self._client:
            return "UNKNOWN"

        prompt = f"{_CLASSIFY_PROMPT}\n\nMessage: {text}"

        try:
            response = self._client.models.generate_content(model=self.model, contents=prompt)

            label = response.text.strip().upper()

            return label if label in INTENT_LABELS else "UNKNOWN"

        except Exception:
            return "UNKNOWN"

    def route(self, intent: str, context: dict) -> list[str]:
        # Maps intent label to list of agent module paths
        agent = AGENT_REGISTRY.get(intent)

        return [agent] if agent else []

    def run(self, text: str, context: dict) -> dict:
        # Full cycle: classify → route → return result shape
        intent = self.classify_intent(text)

        agents = self.route(intent, context)

        return {"intent": intent, "agents": agents, "response": None}
