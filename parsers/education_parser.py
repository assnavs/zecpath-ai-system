"""
Education Parser

Extracts education details from cleaned resume text.
"""

import re

from parsers.education_normalizer import EducationNormalizer
from utils.logger import logger


class EducationParser:

    def __init__(self):

        self.normalizer = EducationNormalizer()

        logger.info("Education Parser initialized.")

    def extract(self, resume_text):

        logger.info("Starting education extraction...")

        educations = []

        lines = [
            line.strip()
            for line in resume_text.split("\n")
            if line.strip()
        ]

        degree_pattern = (
            r"\b("
            r"Bachelor of Technology|"
            r"Bachelor of Engineering|"
            r"Bachelor of Computer Applications|"
            r"Bachelor of Science|"
            r"Bachelor of Commerce|"
            r"Bachelor of Arts|"
            r"Bachelor of Business Administration|"
            r"Master of Technology|"
            r"Master of Engineering|"
            r"Master of Computer Applications|"
            r"Master of Science|"
            r"Master of Commerce|"
            r"Master of Arts|"
            r"Master of Business Administration|"
            r"Doctor of Philosophy|"
            r"B\.?Tech|"
            r"B\.?E|"
            r"BCA|"
            r"B\.?Sc|"
            r"B\.?Com|"
            r"BA|"
            r"BBA|"
            r"M\.?Tech|"
            r"M\.?E|"
            r"MCA|"
            r"M\.?Sc|"
            r"M\.?Com|"
            r"MA|"
            r"MBA|"
            r"PhD"
            r")\b"
        )

        year_pattern = r"(19|20)\d{2}"

        for index, line in enumerate(lines):

            degree_match = re.search(
                degree_pattern,
                line,
                re.IGNORECASE
            )

            if not degree_match:
                continue

            degree = self.normalizer.normalize(
                degree_match.group()
            )

            graduation_year = ""

            year_match = re.search(year_pattern, line)

            if year_match:
                graduation_year = year_match.group()

            institution = ""

            if index + 1 < len(lines):
                institution = lines[index + 1]

            field = ""

            separator = "-"

            if separator in line:

                parts = line.split(separator)

                if len(parts) >= 2:
                    field = re.sub(r"(19|20)\d{2}", "", parts[1]).strip()

            educations.append(
                {
                    "degree": degree,
                    "field": field,
                    "institution": institution,
                    "graduation_year": graduation_year,
                }
            )

        logger.info("Education extraction completed.")

        return {
            "education_count": len(educations),
            "educations": educations,
        }


if __name__ == "__main__":

    sample_resume = """
    EDUCATION

    Master of Computer Applications - Computer Applications 2026
    LEAD College of Management

    Bachelor of Computer Applications - Computer Applications 2024
    Chinmaya College
    """

    parser = EducationParser()

    result = parser.extract(sample_resume)

    print(result)