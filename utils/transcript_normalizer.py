"""
Day 23 - Transcript Normalization Utility

Provides basic normalization for voice transcript text while
preserving the original meaning of the candidate response.
"""

import re


class TranscriptNormalizer:
    """Normalize transcript text for downstream AI processing."""

    @staticmethod
    def normalize_text(text):
        if not isinstance(text, str):
            raise TypeError("Transcript text must be a string.")

        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = normalized.strip()

        return normalized

    @staticmethod
    def normalize_for_matching(text):
        normalized = TranscriptNormalizer.normalize_text(text)
        return normalized.lower()

    @staticmethod
    def normalize_interaction(interaction):
        if not isinstance(interaction, dict):
            raise TypeError("Interaction must be a dictionary.")

        result = dict(interaction)

        if "text" in result:
            result["text"] = TranscriptNormalizer.normalize_text(
                result["text"]
            )

        return result
