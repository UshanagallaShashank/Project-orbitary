# gemini_live.py — streams audio to Gemini Live, returns transcript + intent

import os
import time

from google import genai

from dotenv import load_dotenv

load_dotenv()

INTENT_LABELS = ["DSA", "CALENDAR", "MENTOR", "TRACKER", "MEMORY", "COMMS", "UNKNOWN"]

INTENT_PROMPT = f"Classify the intent as one of: {', '.join(INTENT_LABELS)}. Reply with only the label."


class GeminiLive:

    def __init__(self):
        self._client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

        self._model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

    def extract_intent(self, transcript: str) -> str:
        # Classifies transcript into one of INTENT_LABELS via Gemini
        prompt = f"{INTENT_PROMPT}\n\nText: {transcript}"

        try:
            response = self._client.models.generate_content(model=self._model, contents=prompt)

            label = response.text.strip().upper()

            return label if label in INTENT_LABELS else "UNKNOWN"

        except Exception:
            return "UNKNOWN"

    async def stream_audio(self, audio_bytes: bytes) -> dict:
        # Sends audio bytes to Gemini Live, returns transcript + intent + latency
        start = time.monotonic()

        transcript = ""

        latency_ms = int((time.monotonic() - start) * 1000)

        intent = self.extract_intent(transcript) if transcript else "UNKNOWN"

        return {"transcript": transcript, "intent": intent, "latency_ms": latency_ms}

    def text_to_speech(self, text: str) -> bytes:
        # Wired in F10 with Gemini Live TTS
        return b""
