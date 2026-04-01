# MentorAgent — teaches any concept in a fixed 10-part format via Gemini 2.5

import os

from dotenv import load_dotenv

load_dotenv()

# Teaching format — order is fixed, never changes
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


class MentorAgent:

    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

    def build_prompt(self, topic: str) -> str:
        # Returns the structured 10-part teaching prompt
        parts = "\n".join(f"{i+1}. {p}" for i, p in enumerate(MENTOR_PARTS))

        return f"Teach '{topic}' in exactly this order:\n{parts}"

    def run(self, topic: str, context: dict) -> dict:
        # Stub — replaced in F8 with real Gemini 2.5 call
        return {"topic": topic, "format": MENTOR_PARTS, "response": None}
