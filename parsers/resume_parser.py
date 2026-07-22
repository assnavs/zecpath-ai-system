"""
Resume Parser

Main engine for extracting and cleaning resume text.
"""

import os

from parsers.pdf_reader import extract_pdf_text
from parsers.docx_reader import extract_docx_text
from parsers.text_cleaner import clean_text


def parse_resume(file_path):
    """
    Extract and clean text from a resume.

    Args:
        file_path (str): Path to the resume file.

    Returns:
        str: Cleaned resume text.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        raw_text = extract_pdf_text(file_path)

    elif extension == ".docx":
        raw_text = extract_docx_text(file_path)

    else:
        raise ValueError(f"Unsupported file format: {extension}")

    cleaned_text = clean_text(raw_text)

    return cleaned_text


def save_extracted_text(output_path, text):
    """
    Save cleaned resume text to a text file.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)