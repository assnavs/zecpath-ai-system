"""
Unit Test for Candidate Ranking and Shortlisting
"""

import json

from scoring.candidate_ranking_engine import (
    CandidateRankingEngine
)

from screening_ai.shortlisting import (
    CandidateShortlistingEngine
)


def test_candidate_ranking():

    candidates = [
        {
            "candidate_id": "C001",
            "name": "Candidate A",
            "score": 91
        },
        {
            "candidate_id": "C002",
            "name": "Candidate B",
            "score": 78
        },
        {
            "candidate_id": "C003",
            "name": "Candidate C",
            "score": 56
        },
        {
            "candidate_id": "C004",
            "name": "Candidate D",
            "score": 84
        },
        {
            "candidate_id": "C005",
            "name": "Candidate E",
            "score": 67
        }
    ]

    ranking_engine = CandidateRankingEngine()

    ranking_result = ranking_engine.rank_candidates(
        candidates
    )

    print("\n===== Candidate Ranking Result =====\n")

    print(
        json.dumps(
            ranking_result,
            indent=4
        )
    )

    ranked = ranking_result["ranked_candidates"]

    assert ranking_result["total_candidates"] == 5

    assert ranked[0]["score"] >= ranked[1]["score"]

    assert ranked[0]["rank"] == 1

    assert ranked[-1]["rank"] == 5


def test_candidate_shortlisting():

    candidates = [
        {
            "candidate_id": "C001",
            "name": "Candidate A",
            "score": 91
        },
        {
            "candidate_id": "C002",
            "name": "Candidate B",
            "score": 78
        },
        {
            "candidate_id": "C003",
            "name": "Candidate C",
            "score": 56
        },
        {
            "candidate_id": "C004",
            "name": "Candidate D",
            "score": 84
        },
        {
            "candidate_id": "C005",
            "name": "Candidate E",
            "score": 67
        }
    ]

    engine = CandidateShortlistingEngine()

    result = engine.shortlist_candidates(
        candidates
    )

    print("\n===== Candidate Shortlisting Result =====\n")

    print(
        json.dumps(
            result,
            indent=4
        )
    )

    assert result["total_candidates"] == 5

    assert result["shortlisted_count"] == 2

    assert result["review_count"] == 2

    assert result["rejected_count"] == 1

    ranked = result["ranked_candidates"]

    assert ranked[0]["name"] == "Candidate A"
    assert ranked[0]["decision"] == "Shortlisted"

    assert ranked[1]["name"] == "Candidate D"
    assert ranked[1]["decision"] == "Shortlisted"

    assert ranked[-1]["name"] == "Candidate C"
    assert ranked[-1]["decision"] == "Rejected"

    print(
        "\nAll Candidate Ranking and "
        "Shortlisting tests passed successfully!"
    )


if __name__ == "__main__":

    test_candidate_ranking()

    test_candidate_shortlisting()