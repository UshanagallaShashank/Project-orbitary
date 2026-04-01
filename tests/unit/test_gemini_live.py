# test_gemini_live.py — unit tests for full GeminiLive voice loop

import pytest
from unittest.mock import MagicMock, patch

from voice.gemini_live import INTENT_LABELS


@pytest.fixture
def live():
    # No API key in env — client is None; inject mock manually
    from voice.gemini_live import GeminiLive
    g = GeminiLive()
    g._client = MagicMock()
    return g


# extract_intent — happy path: valid label returned
def test_extract_intent_valid_label(live):
    live._client.models.generate_content.return_value = MagicMock(text="DSA")
    assert live.extract_intent("explain binary search") == "DSA"


# extract_intent — bad response falls back to UNKNOWN
def test_extract_intent_bad_label(live):
    live._client.models.generate_content.return_value = MagicMock(text="GARBAGE")
    assert live.extract_intent("blah") == "UNKNOWN"


# extract_intent — exception returns UNKNOWN
def test_extract_intent_exception(live):
    live._client.models.generate_content.side_effect = Exception("fail")
    assert live.extract_intent("anything") == "UNKNOWN"


# extract_intent — empty string skips Gemini call
def test_extract_intent_empty(live):
    live.extract_intent("")
    live._client.models.generate_content.assert_not_called()


# extract_intent — all valid labels recognised
def test_extract_intent_all_labels(live):
    for label in INTENT_LABELS:
        live._client.models.generate_content.return_value = MagicMock(text=label)
        assert live.extract_intent("some text") == label


# stream_audio — returns required keys
@pytest.mark.asyncio
async def test_stream_audio_keys(live):
    result = await live.stream_audio(b"audio")
    assert set(result.keys()) == {"transcript", "intent", "latency_ms"}


# stream_audio — empty bytes returns UNKNOWN without crashing
@pytest.mark.asyncio
async def test_stream_audio_empty_bytes(live):
    result = await live.stream_audio(b"")
    assert result["intent"] == "UNKNOWN"


# stream_audio — latency is non-negative int
@pytest.mark.asyncio
async def test_stream_audio_latency(live):
    result = await live.stream_audio(b"data")
    assert isinstance(result["latency_ms"], int)
    assert result["latency_ms"] >= 0


# text_to_speech — no client returns empty bytes
def test_tts_no_client():
    from voice.gemini_live import GeminiLive
    g = GeminiLive()
    g._client = None
    assert g.text_to_speech("hello") == b""


# text_to_speech — empty text returns empty bytes
def test_tts_empty_text(live):
    assert live.text_to_speech("") == b""
