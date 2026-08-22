"""
Day 23 - Transcript Data Architecture Tests
"""

import json
from pathlib import Path

from utils.transcript_normalizer import TranscriptNormalizer


BASE_DIR = Path(__file__).resolve().parent.parent
TRANSCRIPT_SCHEMA = BASE_DIR / "data" / "voice_transcript_schema.json"
INTERACTION_SCHEMA = BASE_DIR / "data" / "screening_interaction_schema.json"


def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def test_transcript_schema_exists():
    assert TRANSCRIPT_SCHEMA.exists()


def test_screening_interaction_schema_exists():
    assert INTERACTION_SCHEMA.exists()


def test_required_metadata():
    schema = load_json(TRANSCRIPT_SCHEMA)

    required = schema["required_metadata"]

    expected = [
        "candidate_id",
        "job_id",
        "question_id",
        "timestamp",
        "confidence_level"
    ]

    for field in expected:
        assert field in required


def test_confidence_level_range():
    schema = load_json(TRANSCRIPT_SCHEMA)

    confidence = schema["fields"]["confidence_level"]

    assert confidence["minimum"] == 0.0
    assert confidence["maximum"] == 1.0


def test_speaker_values():
    schema = load_json(TRANSCRIPT_SCHEMA)

    assert schema["fields"]["speaker"]["allowed_values"] == [
        "candidate",
        "interviewer"
    ]


def test_transcript_normalization():
    text = "   Hello    I have   two years experience.   "

    result = TranscriptNormalizer.normalize_text(text)

    assert result == "Hello I have two years experience."


def test_line_break_normalization():
    text = "Python\r\nSQL\r\nMachine Learning"

    result = TranscriptNormalizer.normalize_text(text)

    assert result == "Python SQL Machine Learning"


def test_matching_normalization():
    text = "  Python AND SQL  "

    result = TranscriptNormalizer.normalize_for_matching(text)

    assert result == "python and sql"


def test_interaction_normalization():
    interaction = {
        "candidate_id": "C001",
        "job_id": "JOB001",
        "question_id": "Q001",
        "timestamp": "2026-08-22T10:00:00Z",
        "confidence_level": 0.95,
        "speaker": "candidate",
        "text": "  I   have Python experience.  "
    }

    result = TranscriptNormalizer.normalize_interaction(interaction)

    assert result["text"] == "I have Python experience."
    assert result["candidate_id"] == "C001"
    assert result["confidence_level"] == 0.95


if __name__ == "__main__":
    print("Day 23 Transcript Data Architecture tests")
    print("Run with: python -m tests.test_transcript_data_architecture")
