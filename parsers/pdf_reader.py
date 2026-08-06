"""
PDF Resume Reader

Optimized PDF text extraction using PyMuPDF.

Day 18 improvements:
- Efficient page-wise extraction
- Reduced repeated string allocation
- Context-managed document handling
- Safe empty-page handling
"""

import fitz

from utils.logger import logger


def extract_pdf_text(pdf_path):
    """
    Extract text from a PDF resume efficiently.

    Args:
        pdf_path (str): Path to PDF file.

    Returns:
        str: Extracted resume text.
    """

    if not pdf_path:
        return ""

    try:
        text_parts = []

        with fitz.open(pdf_path) as document:

            for page in document:

                page_text = page.get_text("text")

                if page_text:
                    text_parts.append(page_text)

        extracted_text = "".join(text_parts)

        logger.info(
            "PDF extraction completed successfully."
        )

        return extracted_text

    except Exception as error:

        logger.error(
            f"PDF extraction failed: {error}"
        )

        return ""