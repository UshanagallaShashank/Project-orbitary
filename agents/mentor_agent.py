# mentor_agent.py — teaches any concept in a 10-part format via Gemini 2.5

import os
import json

from dotenv import load_dotenv

load_dotenv()

MENTOR_PARTS = [
    "simple_explanation",
    "analogy",
    "why_it_exists",
    "how_it_works",
    "code_example",
    "step_by_step",
    "use_cases",
    "interview_answer",
    "common_mistakes",
    "quick_summary",
]

_SYSTEM = (
    "You are a world-class DSA and software engineering teacher. "
    "Always respond in valid JSON only — no markdown, no preamble."
)

_FORMAT = json.dumps({p: f"<your {p.replace('_', ' ')} here>" for p in MENTOR_PARTS}, indent=2)


class MentorAgent:

    def __init__(self):
        self._model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

        self._client = self._build_client()

    def _build_client(self):
        api_key = os.getenv("GEMINI_API_KEY", "")

        if not api_key:
            return None

        from google import genai

        return genai.Client(api_key=api_key)

    def build_prompt(self, topic: str) -> str:
        # Returns the structured prompt requesting 10-part JSON response
        return (
            f"Teach the concept '{topic}' by filling every field in this JSON template.\n"
            f"Return ONLY valid JSON. Template:\n{_FORMAT}"
        )

    def teach(self, topic: str) -> dict:
        # Calls Gemini 2.5 and parses the 10-part JSON response
        if not self._client:
            return {"topic": topic, "format": MENTOR_PARTS, "response": None}

        prompt = self.build_prompt(topic)

        try:
            from google.genai import types

            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=_SYSTEM),
            )

            raw = response.text.strip()

            parsed = json.loads(raw)

            return {"topic": topic, "format": MENTOR_PARTS, "response": parsed}

        except Exception:
            return {"topic": topic, "format": MENTOR_PARTS, "response": None}

    def run(self, topic: str, context: dict) -> dict:
        # Entry point called by OrchestratorAgent
        return self.teach(topic)
