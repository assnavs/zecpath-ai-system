"""
Day 24 - Speech-to-Text Integration and Cleaning

Provider-independent speech-to-text processing layer.
The module accepts raw STT output and converts it into
clean, structured transcript data.
"""

import re
from typing import Any, Dict, Optional


class SpeechToTextProcessor:
    """Process raw speech-to-text output for AI analysis."""

    FILLER_WORDS = {
        "um",
        "uh",
        "er",
        "ah",
        "hmm",
        "like",
        "you know",
        "actually",
        "basically",
        "sort of",
        "kind of"
    }

    INTERRUPTION_MARKERS = {
        "[interrupted]",
        "[interruption]",
        "(interrupted)",
        "[cut off]"
    }

    SILENCE_MARKERS = {
        "",
        "[silence]",
        "(silence)",
        "[no speech]",
        "[inaudible]"
    }

    def __init__(self):
        self.last_status = "ready"

    def process(self, raw_text: Optional[str], status: str = "complete") -> Dict[str, Any]:
        """
        Process raw STT output.

        Supported statuses:
        - complete
        - interrupted
        - partial
        - silence
        """

        if raw_text is None:
            raw_text = ""

        if not isinstance(raw_text, str):
            raise TypeError("STT output must be a string or None.")

        normalized_status = status.strip().lower()

        if normalized_status not in {
            "complete",
            "interrupted",
            "partial",
            "silence"
        }:
            raise ValueError(
                "Status must be complete, interrupted, partial, or silence."
            )

        if self.is_silence(raw_text):
            self.last_status = "silence"
            return {
                "text": "",
                "status": "silence",
                "is_partial": False,
                "is_interrupted": False,
                "is_silence": True
            }

        cleaned = self.clean_text(raw_text)

        is_interrupted = (
            normalized_status == "interrupted"
            or self.contains_interruption_marker(raw_text)
        )

        is_partial = normalized_status == "partial"

        if is_interrupted:
            normalized_status = "interrupted"

        self.last_status = normalized_status

        return {
            "text": cleaned,
            "status": normalized_status,
            "is_partial": is_partial,
            "is_interrupted": is_interrupted,
            "is_silence": False
        }

    def clean_text(self, text: str) -> str:
        """Clean transcript text while preserving its meaning."""

        text = self._normalize_whitespace(text)
        text = self._remove_interruption_markers(text)
        text = self._remove_filler_words(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_case(text)
        text = self._correct_punctuation(text)

        return text.strip()

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        text = text.replace("\r\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("\n", " ")
        return re.sub(r"\s+", " ", text).strip()

    def _remove_filler_words(self, text: str) -> str:
        """Remove conversational filler words and nearby punctuation."""

        multi_word_fillers = [
            "you know",
            "sort of",
            "kind of"
        ]

        for filler in multi_word_fillers:
            text = re.sub(
                rf"\b{re.escape(filler)}\b[,;:]?",
                " ",
                text,
                flags=re.IGNORECASE
            )

        single_word_fillers = [
            "um",
            "uh",
            "er",
            "ah",
            "hmm",
            "like",
            "actually",
            "basically"
        ]

        for filler in single_word_fillers:
            text = re.sub(
                rf"\b{re.escape(filler)}\b[,;:]?",
                " ",
                text,
                flags=re.IGNORECASE
            )

        # Remove punctuation accidentally left at the beginning.
        text = re.sub(r"^\s*[,;:]+\s*", "", text)

        # Normalize whitespace after removal.
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def _remove_interruption_markers(text: str) -> str:
        result = text

        markers = [
            "[interrupted]",
            "[interruption]",
            "(interrupted)",
            "[cut off]"
        ]

        for marker in markers:
            result = re.sub(
                re.escape(marker),
                " ",
                result,
                flags=re.IGNORECASE
            )

        return result

    @staticmethod
    def _normalize_case(text: str) -> str:
        """
        Normalize transcript case while preserving technical terms.

        Fully uppercase words are normalized unless they are known
        technical terms or abbreviations.
        """

        if not text:
            return text

        technical_terms = {
            "SQL",
            "Python",
            "Java",
            "JavaScript",
            "TypeScript",
            "C++",
            "C#",
            "HTML",
            "CSS",
            "API",
            "AI",
            "ML",
            "NLP",
            "AWS",
            "Azure",
            "GCP",
            "Power BI",
            "Excel",
            "MySQL",
            "PostgreSQL",
            "MongoDB",
            "Docker",
            "Kubernetes",
            "Git",
            "GitHub"
        }

        for term in sorted(technical_terms, key=len, reverse=True):
            text = re.sub(
                rf"\\b{re.escape(term)}\\b",
                term,
                text,
                flags=re.IGNORECASE
            )

        words = text.split()
        normalized_words = []

        for word in words:
            stripped = word.strip(".,!?;:")

            if (
                stripped
                and stripped.isupper()
                and len(stripped) > 1
                and stripped not in {
                    term.upper() for term in technical_terms
                }
            ):
                word = word.lower()

            normalized_words.append(word)

        text = " ".join(normalized_words)

        if text:
            text = text[0].upper() + text[1:]

        return text

    @staticmethod
    def _correct_punctuation(text: str) -> str:
        text = re.sub(r"\s+([,.!?;:])", r"\1", text)
        text = re.sub(r"([,.!?;:])([A-Za-z])", r"\1 \2", text)

        if text and text[-1] not in ".!?":
            text += "."

        return text

    @classmethod
    def is_silence(cls, text: str) -> bool:
        normalized = text.strip().lower()

        if normalized in cls.SILENCE_MARKERS:
            return True

        return False

    @classmethod
    def contains_interruption_marker(cls, text: str) -> bool:
        normalized = text.strip().lower()

        return any(
            marker in normalized
            for marker in cls.INTERRUPTION_MARKERS
        )


class MockSpeechToTextService:
    """
    Deterministic STT service used for development and testing.

    This provides a provider-independent integration point without
    requiring external API credentials.
    """

    def transcribe(self, audio_input: str) -> Dict[str, Any]:
        if not isinstance(audio_input, str):
            raise TypeError("Audio input must be a string for the mock service.")

        if not audio_input.strip():
            return {
                "text": "",
                "confidence": 0.0,
                "status": "silence"
            }

        return {
            "text": audio_input,
            "confidence": 0.95,
            "status": "complete"
        }


class SpeechToTextIntegration:
    """Connect an STT provider with the transcript cleaning pipeline."""

    def __init__(self, provider=None):
        self.provider = provider or MockSpeechToTextService()
        self.processor = SpeechToTextProcessor()

    def transcribe_and_clean(self, audio_input: str) -> Dict[str, Any]:
        stt_result = self.provider.transcribe(audio_input)

        processed = self.processor.process(
            stt_result.get("text", ""),
            stt_result.get("status", "complete")
        )

        processed["confidence"] = stt_result.get("confidence", 0.0)

        return processed
