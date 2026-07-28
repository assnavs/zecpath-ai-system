"""
Education Relevance Scorer

Assigns relevance categories to extracted education.
"""

import json
from pathlib import Path

from utils.logger import logger


class EducationRelevanceScorer:

    def __init__(self):

        file_path = Path("data/education_relevance.json")

        with open(file_path, "r", encoding="utf-8") as file:
            self.education_map = json.load(file)

    def calculate_relevance(self, candidate_education):

        logger.info("Calculating education relevance...")

        results = []

        for education in candidate_education["educations"]:

            degree = education["degree"]

            relevance = self.education_map.get(
                degree,
                "Other"
            )

            results.append(
                {
                    **education,
                    "relevance": relevance
                }
            )

        return {
            "education_count": len(results),
            "educations": results
        }


if __name__ == "__main__":

    sample = {
        "educations": [
            {
                "degree": "MCA",
                "field": "Computer Applications",
                "institution": "LEAD College",
                "graduation_year": "2026"
            },
            {
                "degree": "BCA",
                "field": "Computer Applications",
                "institution": "Chinmaya College",
                "graduation_year": "2024"
            }
        ]
    }

    scorer = EducationRelevanceScorer()

    print(scorer.calculate_relevance(sample))