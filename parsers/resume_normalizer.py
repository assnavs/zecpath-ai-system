"""
Resume Normalizer

Standardizes resume information before candidate evaluation.

Day 18 improvements:
- Compiled whitespace normalization
- Faster duplicate detection
- Safer nested value handling
- Personal attribute masking
"""

import re

from utils.logger import logger


WHITESPACE_PATTERN = re.compile(r"\s+")


class ResumeNormalizer:
    """
    Normalize resume data and mask non-essential
    personal attributes before evaluation.
    """

    MASK_VALUE = "[MASKED]"

    def __init__(
        self,
        attributes_to_mask=None,
    ):

        self.attributes_to_mask = {
            str(attribute).strip().lower()
            for attribute
            in (attributes_to_mask or [])
        }

        logger.info(
            "Resume Normalizer initialized."
        )

    def normalize_text(self, text):
        """
        Normalize text into a consistent format.
        """

        if text is None:
            return ""

        normalized = WHITESPACE_PATTERN.sub(
            " ",
            str(text),
        ).strip()

        return normalized.lower()

    def normalize_list(self, values):
        """
        Normalize and deduplicate list values
        while preserving original order.
        """

        if values is None:
            return []

        if not isinstance(
            values,
            (list, tuple, set),
        ):
            values = [values]

        normalized_values = []
        seen = set()

        for value in values:

            normalized = self.normalize_text(
                value
            )

            if (
                normalized
                and normalized not in seen
            ):
                seen.add(normalized)
                normalized_values.append(
                    normalized
                )

        return normalized_values

    def normalize_resume(self, resume):
        """
        Normalize a structured resume dictionary.

        Personal attributes configured for masking
        are replaced with [MASKED].
        """

        logger.info(
            "Starting resume normalization..."
        )

        if not isinstance(resume, dict):
            raise TypeError(
                "Resume must be provided "
                "as a dictionary."
            )

        normalized_resume = {}

        for key, value in resume.items():

            normalized_key = (
                str(key)
                .strip()
                .lower()
            )

            if (
                normalized_key
                in self.attributes_to_mask
            ):
                normalized_resume[
                    normalized_key
                ] = self.MASK_VALUE

                continue

            if isinstance(value, str):

                normalized_resume[
                    normalized_key
                ] = self.normalize_text(
                    value
                )

            elif isinstance(
                value,
                (list, tuple, set),
            ):

                normalized_resume[
                    normalized_key
                ] = self.normalize_list(
                    value
                )

            elif isinstance(value, dict):

                normalized_resume[
                    normalized_key
                ] = {
                    str(inner_key)
                    .strip()
                    .lower():
                    self.normalize_text(
                        inner_value
                    )
                    if isinstance(
                        inner_value,
                        str,
                    )
                    else inner_value

                    for (
                        inner_key,
                        inner_value,
                    )
                    in value.items()
                }

            else:

                normalized_resume[
                    normalized_key
                ] = value

        logger.info(
            "Resume normalization completed."
        )

        return normalized_resume