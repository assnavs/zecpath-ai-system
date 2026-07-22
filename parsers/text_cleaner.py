"""
Text Cleaner

This module cleans and normalizes extracted resume text.
"""

import re


def clean_text(text):
    """
    Clean and normalize extracted resume text.

    Args:
        text (str): Raw extracted text.

    Returns:
        str: Cleaned text.
    """

    if not text:
        return ""

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Normalize bullet points
    text = text.replace("•", "-")

    # Normalize section headings
    replacements = {
        "PROFILE": "Profile",
        "WORK EXPERIENCE": "Work Experience",
        "EDUCATION": "Education",
        "SKILLS": "Skills",
        "LANGUAGES": "Languages",
        "CERTIFICATIONS": "Certifications",
        "PROJECTS": "Projects"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text