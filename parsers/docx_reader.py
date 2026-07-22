"""
DOCX Resume Reader

This module extracts text from DOCX resume files using python-docx.
"""

from docx import Document


def extract_docx_text(docx_path):
    """
    Extract text from a DOCX file.

    Args:
        docx_path (str): Path to the DOCX file.

    Returns:
        str: Extracted text.
    """

    extracted_text = ""

    try:
        document = Document(docx_path)

        for paragraph in document.paragraphs:
            extracted_text += paragraph.text + "\n"

        return extracted_text

    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""