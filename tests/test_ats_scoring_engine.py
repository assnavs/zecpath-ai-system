import json

from scoring.ats_scoring_engine import ATSScoringEngine


def test_ats_scoring_engine():
    engine = ATSScoringEngine()

    result = engine.calculate_score(
        job_role="Data Scientist",
        skill_match=90,
        experience_relevance=80,
        education_alignment=75,
        semantic_similarity=85,
    )

    print("\nATS Scoring Result:\n")
    print(json.dumps(result, indent=4))

    assert "job_role" in result
    assert "overall_score" in result
    assert "recommendation" in result
    assert "score_breakdown" in result

    assert result["job_role"] == "Data Scientist"
    assert 0 <= result["overall_score"] <= 100

    print("\nAll ATS Scoring Engine tests passed successfully!")


if __name__ == "__main__":
    test_ats_scoring_engine()