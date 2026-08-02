"""
Resume Normalizer

Standardizes resume information before candidate evaluation.

Features:
- Text normalization
- Whitespace normalization
- Personal attribute masking
- Structured resume normalization
"""

import re

from utils.logger import logger


class ResumeNormalizer:
    """
    Normalize resume data and mask non-essential
    personal attributes before evaluation.
    """

    MASK_VALUE = "[MASKED]"

    def __init__(self, attributes_to_mask=None):

        self.attributes_to_mask = {
            str(attribute).strip().lower()
            for attribute in (attributes_to_mask or [])
        }

        logger.info("Resume Normalizer initialized.")

    def normalize_text(self, text):
        """
        Normalize text into a consistent format.
        """

        if text is None:
            return ""

        text = str(text)

        # Replace repeated whitespace with a single space.
        text = re.sub(r"\s+", " ", text)

        # Remove leading and trailing spaces.
        text = text.strip()

        # Standardize text casing.
        return text.lower()

    def normalize_list(self, values):
        """
        Normalize and deduplicate list values.
        """

        if values is None:
            return []

        if not isinstance(values, list):
            values = [values]

        normalized_values = []
        seen = set()

        for value in values:

            normalized = self.normalize_text(value)

            if normalized and normalized not in seen:

                normalized_values.append(normalized)
                seen.add(normalized)

        return normalized_values

    def normalize_resume(self, resume):
        """
        Normalize a structured resume dictionary.

        Personal attributes configured for masking are
        replaced with [MASKED].
        """

        logger.info("Starting resume normalization...")

        if not isinstance(resume, dict):
            raise TypeError(
                "Resume must be provided as a dictionary."
            )

        normalized_resume = {}

        for key, value in resume.items():

            normalized_key = str(key).strip().lower()

            if normalized_key in self.attributes_to_mask:

                normalized_resume[normalized_key] = self.MASK_VALUE
                continue

            if isinstance(value, str):

                normalized_resume[normalized_key] = (
                    self.normalize_text(value)
                )

            elif isinstance(value, list):

                normalized_resume[normalized_key] = (
                    self.normalize_list(value)
                )

            else:

                normalized_resume[normalized_key] = value

        logger.info("Resume normalization completed.")

        return normalized_resume