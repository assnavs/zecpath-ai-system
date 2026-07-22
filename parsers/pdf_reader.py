"""
PDF Resume Reader

This module extracts text from PDF resume files using PyMuPDF.
"""

import fitz  # PyMuPDF


def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """

    extracted_text = ""

    try:
        document = fitz.open(pdf_path)

        for page in document:
            extracted_text += page.get_text()

        document.close()

        return extracted_text

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""