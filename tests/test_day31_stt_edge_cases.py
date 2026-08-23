from utils.speech_to_text_processor import (
    SpeechToTextProcessor,
    SpeechToTextIntegration,
)


def test_poor_audio():
    processor = SpeechToTextProcessor()

    result = processor.process(
        "I worked with Python",
        status="poor_audio"
    )

    assert result["status"] == "poor_audio"
    assert result["requires_retry"] is True
    assert result["is_edge_case"] is True


def test_language_issue():
    processor = SpeechToTextProcessor()

    result = processor.process(
        "Bonjour",
        status="language_issue"
    )

    assert result["status"] == "language_issue"
    assert result["requires_retry"] is True
    assert result["requires_clarification"] is True


def test_background_noise():
    processor = SpeechToTextProcessor()

    result = processor.process(
        "I have two years of experience",
        status="background_noise"
    )

    assert result["status"] == "background_noise"
    assert result["requires_retry"] is True
    assert result["is_edge_case"] is True


def test_low_confidence_becomes_poor_audio():

    class LowConfidenceProvider:

        def transcribe(self, audio_input):
            return {
                "text": "I worked with SQL",
                "confidence": 0.30,
                "status": "complete"
            }

    integration = SpeechToTextIntegration(
        provider=LowConfidenceProvider()
    )

    result = integration.transcribe_and_clean(
        "audio input"
    )

    assert result["status"] == "poor_audio"
    assert result["confidence"] == 0.30
    assert result["requires_retry"] is True


def test_stt_provider_failure_uses_safe_fallback():

    class FailingProvider:

        def transcribe(self, audio_input):
            raise RuntimeError(
                "STT provider unavailable"
            )

    integration = SpeechToTextIntegration(
        provider=FailingProvider()
    )

    result = integration.transcribe_and_clean(
        "audio input"
    )

    assert result["status"] == "stt_error"
    assert result["fallback"] is True
    assert result["requires_retry"] is True
    assert result["text"] == ""
    assert result["confidence"] == 0.0


def test_normal_transcription_still_works():

    integration = SpeechToTextIntegration()

    result = integration.transcribe_and_clean(
        "I am a data analyst"
    )

    assert result["status"] == "complete"
    assert result["confidence"] == 0.95
    assert result["text"]


def test_silence_still_requires_retry():

    integration = SpeechToTextIntegration()

    result = integration.transcribe_and_clean("")

    assert result["status"] == "silence"
    assert result["requires_retry"] is True
