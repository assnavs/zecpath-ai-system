"""
Certification Parser

Extracts professional certifications from cleaned resume text.
"""

import json
import re
from pathlib import Path

from utils.logger import logger


class CertificationParser:

    def __init__(self):

        dictionary_path = Path("data/certification_dictionary.json")

        with open(dictionary_path, "r", encoding="utf-8") as file:
            self.certification_dictionary = json.load(file)

        logger.info("Certification Parser initialized.")

    def extract(self, resume_text):

        logger.info("Starting certification extraction...")

        certifications = []

        resume_text = resume_text.lower()

        for certificate, details in self.certification_dictionary.items():

            if certificate.lower() in resume_text:

                year = ""

                pattern = (
                    re.escape(certificate)
                    + r".{0,30}?((19|20)\d{2})"
                )

                match = re.search(
                    pattern,
                    resume_text,
                    re.IGNORECASE
                )

                if match:
                    year = match.group(1)

                certifications.append(
                    {
                        "certificate": certificate,
                        "issuer": details["issuer"],
                        "category": details["category"],
                        "year": year,
                    }
                )

        logger.info("Certification extraction completed.")

        return {
            "certification_count": len(certifications),
            "certifications": certifications,
        }


if __name__ == "__main__":

    sample_resume = """
    CERTIFICATIONS

    Google Data Analytics 2024

    AWS Cloud Practitioner 2023

    Cisco CCNA

    Certified Ethical Hacker 2025
    """

    parser = CertificationParser()

    result = parser.extract(sample_resume)

    print(result)