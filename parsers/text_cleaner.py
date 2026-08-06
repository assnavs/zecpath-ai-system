"""
Text Cleaner

Optimized resume text cleaning and noise reduction.

Day 18 improvements:
- Unicode normalization
- Whitespace normalization
- Bullet normalization
- Control-character removal
- Repeated punctuation reduction
- Noisy formatting handling
"""

import re
import unicodedata


# Compile regular expressions once when the module loads.
MULTI_SPACE_PATTERN = re.compile(r"[ \t]+")
MULTI_BLANK_PATTERN = re.compile(r"\n\s*\n+")
CONTROL_CHARACTER_PATTERN = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]"
)
REPEATED_DASH_PATTERN = re.compile(r"-{3,}")
REPEATED_EQUALS_PATTERN = re.compile(r"={3,}")
REPEATED_UNDERSCORE_PATTERN = re.compile(r"_{3,}")


SECTION_REPLACEMENTS = {
    "PROFILE": "Profile",
    "SUMMARY": "Summary",
    "PROFESSIONAL SUMMARY": "Professional Summary",
    "WORK EXPERIENCE": "Work Experience",
    "PROFESSIONAL EXPERIENCE": "Professional Experience",
    "EDUCATION": "Education",
    "SKILLS": "Skills",
    "TECHNICAL SKILLS": "Technical Skills",
    "LANGUAGES": "Languages",
    "CERTIFICATIONS": "Certifications",
    "PROJECTS": "Projects",
}


BULLET_CHARACTERS = (
    "•",
    "●",
    "▪",
    "◦",
    "‣",
    "∙",
)


def clean_text(text):
    """
    Clean and normalize extracted resume text.

    Args:
        text (str): Raw extracted resume text.

    Returns:
        str: Cleaned resume text.
    """

    if not text:
        return ""

    text = str(text)

    # Normalize Unicode representations.
    text = unicodedata.normalize(
        "NFKC",
        text,
    )

    # Normalize line endings.
    text = text.replace(
        "\r\n",
        "\n",
    ).replace(
        "\r",
        "\n",
    )

    # Remove unsupported control characters.
    text = CONTROL_CHARACTER_PATTERN.sub(
        "",
        text,
    )

    # Repair common incorrectly decoded bullet.
    text = text.replace(
        "â€¢",
        "-",
    )

    # Normalize common resume bullet characters.
    for bullet in BULLET_CHARACTERS:
        text = text.replace(
            bullet,
            "-",
        )

    # Reduce decorative separators.
    text = REPEATED_DASH_PATTERN.sub(
        "--",
        text,
    )

    text = REPEATED_EQUALS_PATTERN.sub(
        "==",
        text,
    )

    text = REPEATED_UNDERSCORE_PATTERN.sub(
        "__",
        text,
    )

    # Normalize horizontal whitespace.
    text = MULTI_SPACE_PATTERN.sub(
        " ",
        text,
    )

    # Normalize excessive blank lines.
    text = MULTI_BLANK_PATTERN.sub(
        "\n\n",
        text,
    )

    # Standardize common section headings.
    lines = text.splitlines()

    normalized_lines = []

    for line in lines:

        stripped = line.strip()

        replacement = SECTION_REPLACEMENTS.get(
            stripped.upper()
        )

        if replacement:
            normalized_lines.append(
                replacement
            )
        else:
            normalized_lines.append(
                stripped
            )

    text = "\n".join(
        normalized_lines
    )

    return text.strip()