"""
Day 20 - ATS Live Demo

Demonstrates the existing ATS workflow using
synthetic candidate profiles.

The demo:
1. Loads the Day 20 demo dataset.
2. Calculates candidate evaluation inputs.
3. Uses the existing ATS Scoring Engine.
4. Uses the existing Candidate Ranking Engine.
5. Uses the existing Candidate Shortlisting Engine.
6. Displays recruiter-friendly final results.
"""

import json
from pathlib import Path

from scoring.ats_scoring_engine import ATSScoringEngine

from scoring.candidate_ranking_engine import (
    CandidateRankingEngine,
)

from screening_ai.shortlisting import (
    CandidateShortlistingEngine,
)


def load_demo_data():
    """
    Load the synthetic Day 20 demo dataset.
    """

    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "demo"
        / "demo_candidates.json"
    )

    with open(
        data_path,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def calculate_skill_match(
    candidate_skills,
    required_skills,
):
    """
    Calculate percentage overlap between
    candidate and required skills.
    """

    candidate_set = {
        str(skill).strip().lower()
        for skill in candidate_skills
    }

    required_set = {
        str(skill).strip().lower()
        for skill in required_skills
    }

    if not required_set:
        return 0.0

    matched_skills = (
        candidate_set
        & required_set
    )

    score = (
        len(matched_skills)
        / len(required_set)
    ) * 100

    return round(
        score,
        2,
    )


def get_demo_component_scores(
    candidate,
    required_skills,
):
    """
    Generate controlled evaluation inputs
    for the Day 20 demonstration.

    Skill match is calculated from the
    synthetic dataset.

    Other component values are controlled
    demo inputs representing strong,
    moderate, and low candidate relevance.

    The actual final ATS score is calculated
    by the existing ATS Scoring Engine.
    """

    skill_match = calculate_skill_match(
        candidate.get(
            "skills",
            [],
        ),
        required_skills,
    )

    profile_type = candidate.get(
        "profile_type",
        "",
    )

    if profile_type == "Strong Match":

        return {
            "skill_match": skill_match,
            "experience_relevance": 90.0,
            "education_alignment": 90.0,
            "semantic_similarity": 92.0,
        }

    if profile_type == "Moderate Match":

        return {
            "skill_match": skill_match,
            "experience_relevance": 72.0,
            "education_alignment": 75.0,
            "semantic_similarity": 76.0,
        }

    return {
        "skill_match": skill_match,
        "experience_relevance": 40.0,
        "education_alignment": 65.0,
        "semantic_similarity": 35.0,
    }


def run_demo():
    """
    Run the complete Day 20 ATS demonstration.
    """

    print(
        "\n=========================================="
    )

    print(
        "          ZECPATH AI - ATS LIVE DEMO"
    )

    print(
        "=========================================="
    )

    # -----------------------------------------
    # Load demo dataset
    # -----------------------------------------

    demo_data = load_demo_data()

    demo_job = demo_data[
        "demo_job"
    ]

    job_role = demo_job[
        "job_role"
    ]

    required_skills = demo_job[
        "job_description"
    ][
        "skills"
    ]

    candidates = demo_data[
        "candidates"
    ]

    print(
        f"\nTarget Job Role: {job_role}"
    )

    print(
        f"Candidates Evaluated: "
        f"{len(candidates)}"
    )

    print(
        "\nRequired Skills:"
    )

    for skill in required_skills:
        print(
            f"  - {skill}"
        )

    # -----------------------------------------
    # Initialize existing ATS components
    # -----------------------------------------

    scoring_engine = (
        ATSScoringEngine()
    )

    ranking_engine = (
        CandidateRankingEngine()
    )

    shortlisting_engine = (
        CandidateShortlistingEngine()
    )

    scored_candidates = []

    # -----------------------------------------
    # Candidate scoring
    # -----------------------------------------

    print(
        "\n=========================================="
    )

    print(
        "            CANDIDATE SCORING"
    )

    print(
        "=========================================="
    )

    for candidate in candidates:

        component_scores = (
            get_demo_component_scores(
                candidate,
                required_skills,
            )
        )

        scoring_result = (
            scoring_engine.calculate_score(
                job_role=job_role,
                **component_scores,
            )
        )

        scored_candidate = {
            "candidate_id": candidate[
                "candidate_id"
            ],
            "name": candidate[
                "name"
            ],
            "score": scoring_result[
                "overall_score"
            ],
        }

        scored_candidates.append(
            scored_candidate
        )

        print(
            f"\nCandidate: "
            f"{candidate['name']}"
        )

        print(
            f"Candidate ID: "
            f"{candidate['candidate_id']}"
        )

        print(
            f"Profile Type: "
            f"{candidate['profile_type']}"
        )

        print(
            f"Skill Match: "
            f"{component_scores['skill_match']}%"
        )

        print(
            f"Experience Relevance: "
            f"{component_scores['experience_relevance']}%"
        )

        print(
            f"Education Alignment: "
            f"{component_scores['education_alignment']}%"
        )

        print(
            f"Semantic Similarity: "
            f"{component_scores['semantic_similarity']}%"
        )

        print(
            f"Overall ATS Score: "
            f"{scoring_result['overall_score']}"
        )

        print(
            f"Recommendation: "
            f"{scoring_result['recommendation']}"
        )

    # -----------------------------------------
    # Candidate ranking
    # -----------------------------------------

    ranked_result = (
        ranking_engine.rank_candidates(
            scored_candidates
        )
    )

    # The ranking engine may return either
    # a list or a dictionary containing the list.
    if isinstance(
        ranked_result,
        dict,
    ):
        ranked_candidates = (
            ranked_result.get(
                "ranked_candidates",
                [],
            )
        )
    else:
        ranked_candidates = (
            ranked_result
        )

    # -----------------------------------------
    # Candidate shortlisting
    # -----------------------------------------

    shortlist_result = (
        shortlisting_engine.shortlist_candidates(
            ranked_candidates
        )
    )

    if isinstance(
        shortlist_result,
        dict,
    ):
        final_candidates = (
            shortlist_result.get(
                "ranked_candidates",
                ranked_candidates,
            )
        )
    else:
        final_candidates = (
            shortlist_result
        )

    # -----------------------------------------
    # Final output
    # -----------------------------------------

    print(
        "\n=========================================="
    )

    print(
        "        RANKING & SHORTLISTING"
    )

    print(
        "=========================================="
    )

    for candidate in final_candidates:

        print(
            f"\nRank {candidate.get('rank', '-')}"
            f" | {candidate.get('name', 'Unknown')}"
        )

        print(
            f"Candidate ID: "
            f"{candidate.get('candidate_id', '-')}"
        )

        print(
            f"ATS Score: "
            f"{candidate.get('score', 0)}"
        )

        print(
            f"Decision: "
            f"{candidate.get('decision', '-')}"
        )

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    shortlisted_count = sum(
        1
        for candidate in final_candidates
        if candidate.get(
            "decision"
        ) == "Shortlisted"
    )

    review_count = sum(
        1
        for candidate in final_candidates
        if candidate.get(
            "decision"
        ) == "Review"
    )

    rejected_count = sum(
        1
        for candidate in final_candidates
        if candidate.get(
            "decision"
        ) == "Rejected"
    )

    print(
        "\n=========================================="
    )

    print(
        "               DEMO SUMMARY"
    )

    print(
        "=========================================="
    )

    print(
        f"\nTotal Candidates: "
        f"{len(final_candidates)}"
    )

    print(
        f"Shortlisted: "
        f"{shortlisted_count}"
    )

    print(
        f"Review: "
        f"{review_count}"
    )

    print(
        f"Rejected: "
        f"{rejected_count}"
    )

    print(
        "\nATS live demonstration "
        "completed successfully!"
    )


if __name__ == "__main__":
    run_demo()