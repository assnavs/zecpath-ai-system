"""
Unit Test for Experience Parser and Experience Relevance Scorer
"""

import json

from parsers.experience_parser import ExperienceParser
from scoring.experience_relevance_scorer import ExperienceRelevanceScorer


def test_experience_parser():

    sample_resume = """
ABC Technologies
Data Analyst
Jan 2022 - Dec 2023

XYZ Solutions
Business Analyst
Jan 2024 - Present
"""

    parser = ExperienceParser()

    experience = parser.extract(sample_resume)

    print("\n===== Experience Parsing Result =====\n")
    print(json.dumps(experience, indent=4))

    assert experience["experience_count"] == 2
    assert experience["total_experience_months"] > 0

    scorer = ExperienceRelevanceScorer()

    result = scorer.calculate_relevance(
        experience,
        "Data Analyst"
    )

    print("\n===== Experience Relevance =====\n")
    print(json.dumps(result, indent=4))

    assert result["relevance_score"] > 0
    assert result["target_role"] == "Data Analyst"

    print("\nAll Experience Parser Tests Passed.\n")


if __name__ == "__main__":
    test_experience_parser()