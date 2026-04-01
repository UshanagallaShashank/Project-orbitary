# OrchestratorAgent — routes intent to the right agent(s) via Gemini 2.5 + ADK

import os

from dotenv import load_dotenv

load_dotenv()

# Intent labels Orbit understands
INTENT_LABELS = ["DSA", "CALENDAR", "MENTOR", "TRACKER", "MEMORY", "COMMS", "UNKNOWN"]

# Maps each intent to its agent module name
AGENT_REGISTRY = {
    "DSA": "agents.tracker_agent",
    "CALENDAR": "agents.task_agent",
    "MENTOR": "agents.mentor_agent",
    "TRACKER": "agents.tracker_agent",
    "MEMORY": "agents.memory_agent",
    "COMMS": "agents.comms_agent",
}


class OrchestratorAgent:

    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

    def classify_intent(self, text: str) -> str:
        # Stub — replaced in F3 with real Gemini 2.5 call
        return "UNKNOWN"

    def route(self, intent: str, context: dict) -> list[str]:
        # Returns list of agent module names to call
        agent = AGENT_REGISTRY.get(intent)

        return [agent] if agent else []

    def run(self, text: str, context: dict) -> dict:
        # Full orchestration: classify → route → merge
        intent = self.classify_intent(text)

        agents = self.route(intent, context)

        return {"intent": intent, "agents": agents, "response": None}
