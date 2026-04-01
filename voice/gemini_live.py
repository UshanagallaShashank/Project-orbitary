# gemini_live.py — streams audio to Gemini Live, returns transcript + intent

import os

from dotenv import load_dotenv

load_dotenv()

LIVE_MODEL = os.getenv("GEMINI_LIVE_MODEL", "gemini-2.0-flash-live-001")

INTENT_LABELS = ["DSA", "CALENDAR", "MENTOR", "TRACKER", "MEMORY", "COMMS", "UNKNOWN"]


class GeminiLive:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")

        self.model = LIVE_MODEL

    def stream_audio(self, audio_bytes: bytes) -> dict:
        # Stub — replaced in F2 with real Gemini Live stream
        return {"transcript": "", "intent": "UNKNOWN", "latency_ms": 0}

    def text_to_speech(self, text: str) -> bytes:
        # Stub — replaced in F10 with real TTS output
        return b""

    def extract_intent(self, transcript: str) -> str:
        # Classifies raw transcript into one of INTENT_LABELS
        # Stub — replaced in F2 with real Gemini Live response parsing
        return "UNKNOWN"
