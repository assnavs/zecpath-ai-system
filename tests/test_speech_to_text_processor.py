"""
Day 24 - Speech-to-Text Integration and Cleaning Tests
"""

import json
from pathlib import Path

from utils.speech_to_text_processor import (
    MockSpeechToTextService,
    SpeechToTextIntegration,
    SpeechToTextProcessor
)


BASE_DIR = Path(__file__).resolve().parent.parent
TEST_CASES = BASE_DIR / "data" / "stt_test_cases.json"


def load_test_cases():
    with open(TEST_CASES, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def test_stt_test_cases_exist():
    assert TEST_CASES.exists()


def test_filler_word_removal():
    processor = SpeechToTextProcessor()

    result = processor.clean_text(
        "Um, I basically have experience in Python"
    )

    assert result == "I have experience in Python."


def test_whitespace_cleanup():
    processor = SpeechToTextProcessor()

    result = processor.clean_text(
        "I   have    experience   in   SQL"
    )

    assert result == "I have experience in SQL."


def test_case_normalization():
    processor = SpeechToTextProcessor()

    result = processor.clean_text(
        "i have EXPERIENCE in python"
    )

    assert result == "I have experience in python."


def test_punctuation_correction():
    processor = SpeechToTextProcessor()

    result = processor.clean_text(
        "I have experience in Python and SQL"
    )

    assert result == "I have experience in Python and SQL."


def test_interrupted_speech():
    processor = SpeechToTextProcessor()

    result = processor.process(
        "I worked on machine learning [interrupted]",
        status="interrupted"
    )

    assert result["status"] == "interrupted"
    assert result["is_interrupted"] is True
    assert "interrupted" not in result["text"].lower()


def test_partial_answer():
    processor = SpeechToTextProcessor()

    result = processor.process(
        "I have worked with Python and SQL",
        status="partial"
    )

    assert result["status"] == "partial"
    assert result["is_partial"] is True


def test_silence_detection():
    processor = SpeechToTextProcessor()

    result = processor.process(
        "[silence]",
        status="silence"
    )

    assert result["status"] == "silence"
    assert result["is_silence"] is True
    assert result["text"] == ""


def test_mock_stt_service():
    service = MockSpeechToTextService()

    result = service.transcribe(
        "I have two years of experience in Python"
    )

    assert result["status"] == "complete"
    assert result["confidence"] == 0.95
    assert result["text"]


def test_stt_integration_pipeline():
    integration = SpeechToTextIntegration()

    result = integration.transcribe_and_clean(
        "Um, I have two years of experience in Python"
    )

    assert result["status"] == "complete"
    assert result["confidence"] == 0.95
    assert result["text"] == "I have two years of experience in Python."


def test_multiple_stt_test_cases():
    cases = load_test_cases()["cases"]

    assert len(cases) >= 7

    for case in cases:
        assert "case_id" in case
        assert "condition" in case
        assert "input" in case


if __name__ == "__main__":
    print("Run with:")
    print("python -m pytest tests/test_speech_to_text_processor.py -v")
