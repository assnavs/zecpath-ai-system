"""
Job Description Cleaner

This module cleans and normalizes extracted job description text.
"""

import re


def clean_job_description(text):
    """
    Clean and normalize job description text.

    Args:
        text (str): Raw job description text.

    Returns:
        str: Cleaned job description.
    """

    if not text:
        return ""

    # Remove extra spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Normalize bullet points
    text = text.replace("•", "-")
    text = text.replace("", "-")

    # Normalize common headings
    replacements = {
        "RESPONSIBILITIES": "Responsibilities",
        "REQUIREMENTS": "Requirements",
        "QUALIFICATIONS": "Qualifications",
        "SKILLS": "Skills",
        "EXPERIENCE": "Experience",
        "EDUCATION": "Education"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text