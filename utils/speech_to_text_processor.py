import re
from typing import Any, Dict, Optional


class SpeechToTextProcessor:
    """
    Process raw speech-to-text output for AI analysis.

    Supports normal responses as well as Day 31 edge cases:
    - poor audio
    - language issue
    - background noise
    - interrupted speech
    - partial response
    - silence
    """

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

    EDGE_CASE_STATUSES = {
        "complete",
        "interrupted",
        "partial",
        "silence",
        "poor_audio",
        "language_issue",
        "background_noise"
    }

    def __init__(self):
        self.last_status = "ready"

    def process(
        self,
        raw_text: Optional[str],
        status: str = "complete"
    ) -> Dict[str, Any]:

        if raw_text is None:
            raw_text = ""

        if not isinstance(raw_text, str):
            raise TypeError(
                "STT output must be a string or None."
            )

        normalized_status = (
            str(status).strip().lower()
        )

        if normalized_status not in self.EDGE_CASE_STATUSES:
            raise ValueError(
                "Unsupported STT status."
            )

        if self.is_silence(raw_text):
            self.last_status = "silence"

            return {
                "text": "",
                "status": "silence",
                "is_partial": False,
                "is_interrupted": False,
                "is_silence": True,
                "requires_retry": True,
                "requires_clarification": False,
                "is_edge_case": True
            }

        cleaned = self.clean_text(raw_text)

        is_interrupted = (
            normalized_status == "interrupted"
            or self.contains_interruption_marker(raw_text)
        )

        is_partial = normalized_status == "partial"

        if is_interrupted:
            normalized_status = "interrupted"

        edge_case = normalized_status in {
            "poor_audio",
            "language_issue",
            "background_noise"
        }

        self.last_status = normalized_status

        return {
            "text": cleaned,
            "status": normalized_status,
            "is_partial": is_partial,
            "is_interrupted": is_interrupted,
            "is_silence": False,
            "requires_retry": edge_case or is_interrupted,
            "requires_clarification": (
                normalized_status == "language_issue"
            ),
            "is_edge_case": edge_case
        }

    def clean_text(self, text: str) -> str:

        if not isinstance(text, str):
            raise TypeError(
                "Text must be a string."
            )

        text = text.strip()

        for filler in sorted(
            self.FILLER_WORDS,
            key=len,
            reverse=True
        ):
            text = re.sub(
                rf"\b{re.escape(filler)}\b[,\s]*",
                "",
                text,
                flags=re.IGNORECASE
            )

        for marker in self.INTERRUPTION_MARKERS:
            text = re.sub(
                re.escape(marker),
                "",
                text,
                flags=re.IGNORECASE
            )

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        if not text:
            return ""

        words = text.split()
        normalized_words = []

        technical_terms = {
            "python",
            "sql",
            "java",
            "javascript",
            "power bi",
            "api",
            "ai",
            "ml",
            "aws",
            "azure",
            "docker"
        }

        for word in words:
            stripped = word.strip(
                ".,!?;:"
            )

            if (
                stripped
                and stripped.isupper()
                and len(stripped) > 1
                and stripped not in {
                    term.upper()
                    for term in technical_terms
                }
            ):
                word = word.lower()

            normalized_words.append(word)

        text = " ".join(normalized_words)

        if text:
            text = (
                text[0].upper()
                + text[1:]
            )

        text = re.sub(
            r"\s+([,.!?;:])",
            r"\1",
            text
        )

        if text and text[-1] not in ".!?":
            text += "."

        return text

    @classmethod
    def is_silence(cls, text: str) -> bool:
        return (
            text.strip().lower()
            in cls.SILENCE_MARKERS
        )

    @classmethod
    def contains_interruption_marker(
        cls,
        text: str
    ) -> bool:

        normalized = text.strip().lower()

        return any(
            marker in normalized
            for marker in cls.INTERRUPTION_MARKERS
        )


class MockSpeechToTextService:

    def transcribe(
        self,
        audio_input: str
    ) -> Dict[str, Any]:

        if not isinstance(audio_input, str):
            raise TypeError(
                "Audio input must be a string "
                "for the mock service."
            )

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
    """
    Connect an STT provider with transcript processing.

    Includes safe fallback behaviour for provider failures.
    """

    LOW_CONFIDENCE_THRESHOLD = 0.60

    def __init__(self, provider=None):
        self.provider = (
            provider
            or MockSpeechToTextService()
        )
        self.processor = SpeechToTextProcessor()

    def transcribe_and_clean(
        self,
        audio_input: str
    ) -> Dict[str, Any]:

        try:
            stt_result = self.provider.transcribe(
                audio_input
            )

            confidence = float(
                stt_result.get(
                    "confidence",
                    0.0
                )
            )

            status = stt_result.get(
                "status",
                "complete"
            )

            if (
                status == "complete"
                and confidence
                < self.LOW_CONFIDENCE_THRESHOLD
            ):
                status = "poor_audio"

            processed = self.processor.process(
                stt_result.get(
                    "text",
                    ""
                ),
                status
            )

            processed["confidence"] = confidence

            return processed

        except Exception as exc:

            return {
                "text": "",
                "confidence": 0.0,
                "status": "stt_error",
                "is_partial": False,
                "is_interrupted": False,
                "is_silence": False,
                "is_edge_case": True,
                "requires_retry": True,
                "requires_clarification": False,
                "fallback": True,
                "error": str(exc)
            }
