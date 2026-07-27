"""
Experience Parser

Extracts work experience information from cleaned resume text.
"""

import re
from datetime import datetime

from utils.logger import logger


MONTHS = (
    "jan|january|feb|february|mar|march|apr|april|may|"
    "jun|june|jul|july|aug|august|sep|sept|september|"
    "oct|october|nov|november|dec|december"
)


class ExperienceParser:

    def __init__(self):
        logger.info("Experience Parser initialized.")

    def extract(self, resume_text):

        logger.info("Starting experience extraction...")

        experiences = []

        lines = [line.strip() for line in resume_text.split("\n") if line.strip()]

        i = 0

        while i < len(lines):

            line = lines[i]

            date_pattern = (
                  r"((?:Jan|January|Feb|February|Mar|March|Apr|April|May|"
                  r"Jun|June|Jul|July|Aug|August|Sep|Sept|September|"
                  r"Oct|October|Nov|November|Dec|December)\s+\d{4})"
                  r"\s*[-–]\s*"
                  r"(Present|Current|(?:Jan|January|Feb|February|Mar|March|Apr|April|May|"
                  r"Jun|June|Jul|July|Aug|August|Sep|Sept|September|"
                  r"Oct|October|Nov|November|Dec|December)\s+\d{4})"
            )

            date_match = re.search(
                date_pattern,
                line,
                re.IGNORECASE
            )

            if date_match:

                company = lines[i - 2] if i >= 2 else ""

                job_title = lines[i - 1] if i >= 1 else ""

                start_date = date_match.group(1)
                end_date = date_match.group(2)

                duration = self.calculate_duration(start_date, end_date)

                experiences.append(
                    {
                        "company": company,
                        "job_title": job_title,
                        "start_date": start_date,
                        "end_date": end_date,
                        "duration_months": duration,
                    }
                )

            i += 1

        logger.info("Experience extraction completed.")

        return {
            "total_experience_months": self.total_experience(experiences),
            "experience_count": len(experiences),
            "experiences": experiences,
        }

    def calculate_duration(self, start, end):

        start_date = self.parse_date(start)

        if end.lower() in ["present", "current"]:
            end_date = datetime.today()
        else:
            end_date = self.parse_date(end)

        months = (
            (end_date.year - start_date.year) * 12
            + (end_date.month - start_date.month)
        )

        return max(months, 0)

    def parse_date(self, value):

        formats = [
            "%b %Y",
            "%B %Y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value.strip(), fmt)
            except ValueError:
                pass

        return datetime.today()

    def total_experience(self, experiences):

        return sum(item["duration_months"] for item in experiences)