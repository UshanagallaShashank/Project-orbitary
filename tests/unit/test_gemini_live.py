# test_gemini_live.py — unit tests for GeminiLive voice module

import pytest
from unittest.mock import MagicMock, patch


# Patch genai.Client before import so no real key is needed
@pytest.fixture
def live():
    with patch("voice.gemini_live.genai.Client") as mock_cls:
        mock_cls.return_value = MagicMock()
        from voice.gemini_live import GeminiLive
        instance = GeminiLive()
        yield instance


from voice.gemini_live import INTENT_LABELS


# extract_intent — happy path: valid label returned
def test_extract_intent_valid_label(live):
    live._client.models.generate_content.return_value = MagicMock(text="DSA")
    result = live.extract_intent("explain binary search")
    assert result == "DSA"


# extract_intent — edge case: unrecognised label falls back to UNKNOWN
def test_extract_intent_unknown_label(live):
    live._client.models.generate_content.return_value = MagicMock(text="GIBBERISH")
    result = live.extract_intent("random text")
    assert result == "UNKNOWN"


# extract_intent — failure: exception returns UNKNOWN
def test_extract_intent_exception(live):
    live._client.models.generate_content.side_effect = Exception("api error")
    result = live.extract_intent("explain trees")
    assert result == "UNKNOWN"


# extract_intent — all valid labels are recognised
def test_extract_intent_all_labels(live):
    for label in INTENT_LABELS:
        live._client.models.generate_content.return_value = MagicMock(text=label)
        result = live.extract_intent("some text")
        assert result == label


# stream_audio — happy path: returns required keys
@pytest.mark.asyncio
async def test_stream_audio_returns_keys(live):
    result = await live.stream_audio(b"fake_audio")
    assert "transcript" in result
    assert "intent" in result
    assert "latency_ms" in result


# stream_audio — empty audio returns UNKNOWN intent
@pytest.mark.asyncio
async def test_stream_audio_empty_bytes(live):
    result = await live.stream_audio(b"")
    assert result["intent"] == "UNKNOWN"


# stream_audio — latency is a non-negative integer
@pytest.mark.asyncio
async def test_stream_audio_latency_non_negative(live):
    result = await live.stream_audio(b"audio")
    assert isinstance(result["latency_ms"], int)
    assert result["latency_ms"] >= 0


# text_to_speech — returns bytes
def test_text_to_speech_returns_bytes(live):
    result = live.text_to_speech("hello world")
    assert isinstance(result, bytes)
