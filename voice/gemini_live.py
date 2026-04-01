# gemini_live.py — full voice loop: audio in, transcript + intent out, TTS back

import os
import time
import asyncio

from google import genai
from google.genai import types

from dotenv import load_dotenv

load_dotenv()

INTENT_LABELS = ["DSA", "CALENDAR", "MENTOR", "TRACKER", "MEMORY", "COMMS", "UNKNOWN"]

_CLASSIFY = f"Classify the intent as exactly one of: {', '.join(INTENT_LABELS)}. Reply with only the label."


class GeminiLive:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "")

        self._client = genai.Client(api_key=api_key) if api_key else None

        self._model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")

        self._live_model = os.getenv("GEMINI_LIVE_MODEL", "gemini-2.0-flash-live-001")

    def extract_intent(self, transcript: str) -> str:
        # Classifies transcript into one INTENT_LABEL via Gemini
        if not transcript or not self._client:
            return "UNKNOWN"

        try:
            resp = self._client.models.generate_content(
                model=self._model, contents=f"{_CLASSIFY}\n\nText: {transcript}"
            )

            label = resp.text.strip().upper()

            return label if label in INTENT_LABELS else "UNKNOWN"

        except Exception:
            return "UNKNOWN"

    async def stream_audio(self, audio_bytes: bytes) -> dict:
        # Sends PCM audio to Gemini Live, returns transcript + intent + latency
        start = time.monotonic()

        transcript = ""

        if self._client and audio_bytes:
            try:
                config = types.LiveConnectConfig(response_modalities=["TEXT"])

                async with self._client.aio.live.connect(model=self._live_model, config=config) as session:
                    await session.send(input={"data": audio_bytes, "mime_type": "audio/pcm"}, end_of_turn=True)

                    async for resp in session.receive():
                        if resp.text:
                            transcript += resp.text

            except Exception:
                transcript = ""

        latency_ms = int((time.monotonic() - start) * 1000)

        intent = self.extract_intent(transcript)

        return {"transcript": transcript, "intent": intent, "latency_ms": latency_ms}

    def text_to_speech(self, text: str) -> bytes:
        # Returns synthesised audio bytes via Gemini Live TTS
        if not self._client or not text:
            return b""

        try:
            config = types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")
                )),
            )

            resp = self._client.models.generate_content(
                model=self._live_model, contents=text, config=config
            )

            parts = resp.candidates[0].content.parts

            return parts[0].inline_data.data if parts else b""

        except Exception:
            return b""
