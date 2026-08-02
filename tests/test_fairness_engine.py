"""
Unit Test for Fairness, Normalization and Bias Reduction
"""

import json

from scoring.fair_scoring_engine import FairScoringEngine


def test_fairness_engine():

    engine = FairScoringEngine()

    sample_resume = {
        "name": "Candidate A",
        "email": "candidate@example.com",
        "phone": "9876543210",
        "gender": "Female",
        "nationality": "Indian",
        "summary":
            "  DATA   SCIENTIST with experience in "
            "Machine Learning and Analytics.  ",
        "skills": [
            "PYTHON",
            " SQL ",
            "Machine Learning",
            "python"
        ],
        "experience":
            "  Worked as a DATA ANALYST for two years. "
    }

    sample_scores = {
        "keyword_match": 96,
        "experience_relevance": 82,
        "education_alignment": 78,
        "semantic_similarity": 88
    }

    scoring_weights = {
        "keyword_match": 0.40,
        "experience_relevance": 0.20,
        "education_alignment": 0.10,
        "semantic_similarity": 0.30
    }

    result = engine.evaluate_candidate(
        resume=sample_resume,
        scores=sample_scores,
        scoring_weights=scoring_weights
    )

    print(
        "\n===== Fairness Evaluation Result =====\n"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    normalized_resume = result[
        "normalized_resume"
    ]

    normalized_scores = result[
        "normalized_scores"
    ]

    bias_indicators = result[
        "bias_indicators"
    ]

    # Personal attribute masking tests

    assert normalized_resume["name"] == "[MASKED]"
    assert normalized_resume["email"] == "[MASKED]"
    assert normalized_resume["phone"] == "[MASKED]"
    assert normalized_resume["gender"] == "[MASKED]"
    assert normalized_resume["nationality"] == "[MASKED]"

    # Text normalization tests

    assert normalized_resume["summary"] == (
        "data scientist with experience in "
        "machine learning and analytics."
    )

    assert normalized_resume["skills"] == [
        "python",
        "sql",
        "machine learning"
    ]

    # Score normalization and keyword cap tests

    assert normalized_scores[
        "keyword_match"
    ] == 85.0

    assert normalized_scores[
        "experience_relevance"
    ] == 82.0

    assert normalized_scores[
        "education_alignment"
    ] == 78.0

    assert normalized_scores[
        "semantic_similarity"
    ] == 88.0

    # Fairness indicator tests

    assert result[
        "fairness_controls"
    ]["score_normalized"] is True

    assert result[
        "fairness_controls"
    ]["personal_attributes_masked"] is True

    assert bias_indicators[
        "keyword_dependency_reduced"
    ] is True

    assert bias_indicators[
        "semantic_contribution_sufficient"
    ] is True

    assert bias_indicators[
        "requires_review"
    ] is False

    print(
        "\nAll Fairness, Normalization and "
        "Bias Reduction tests passed successfully!"
    )


if __name__ == "__main__":
    test_fairness_engine()