"""
Unit Test for Education Parser
"""

import json

from parsers.education_parser import EducationParser
from scoring.education_relevance_scorer import EducationRelevanceScorer


def test_education_parser():

    sample_resume = """
    LEAD College of Management
    Master of Computer Applications
    2024 - 2026

    Chinmaya College
    Bachelor of Computer Applications
    2021 - 2024
    """

    parser = EducationParser()

    education = parser.extract(sample_resume)

    print("\n===== Education Parsing Result =====\n")
    print(json.dumps(education, indent=4))

    assert education["education_count"] == 2

    scorer = EducationRelevanceScorer()

    result = scorer.calculate_relevance(education)

    print("\n===== Education Relevance =====\n")
    print(json.dumps(result, indent=4))

    assert result["education_count"] == 2

    assert result["educations"][0]["degree"] == "MCA"
    assert result["educations"][1]["degree"] == "BCA"

    assert result["educations"][0]["relevance"] == "Computer Science"
    assert result["educations"][1]["relevance"] == "Computer Science"

    print("\nAll Education Parser Tests Passed.\n")


if __name__ == "__main__":
    test_education_parser()