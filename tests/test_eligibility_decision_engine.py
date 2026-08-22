"""
Day 21 - Eligibility Decision Engine Tests
"""

from scoring.eligibility_decision_engine import (
    EligibilityDecisionEngine
)


def test_eligible_candidate():

    engine = EligibilityDecisionEngine()

    ats_result = {
        "overall_score": 92.5
    }

    candidate = {
        "candidate_id": "ELG001",
        "name": "Candidate Eligible",
        "skills": [
            "Python",
            "SQL",
            "Machine Learning"
        ],
        "experience_years": 2,
        "location": "Remote",
        "availability": "Immediate"
    }

    result = engine.evaluate_candidate(
        "Data Scientist",
        ats_result,
        candidate
    )

    assert result["eligibility"] == "ELIGIBLE"
    assert result["ats_score"] == 92.5


def test_review_candidate():

    engine = EligibilityDecisionEngine()

    ats_result = {
        "overall_score": 68
    }

    candidate = {
        "candidate_id": "ELG002",
        "name": "Candidate Review",
        "skills": [
            "Python",
            "SQL"
        ],
        "experience_years": 1,
        "location": "Remote",
        "availability": "Immediate"
    }

    result = engine.evaluate_candidate(
        "Data Scientist",
        ats_result,
        candidate
    )

    assert result["eligibility"] == "REVIEW"


def test_rejected_candidate():

    engine = EligibilityDecisionEngine()

    ats_result = {
        "overall_score": 40
    }

    candidate = {
        "candidate_id": "ELG003",
        "name": "Candidate Rejected",
        "skills": [
            "HTML",
            "CSS"
        ],
        "experience_years": 0,
        "location": "Remote",
        "availability": "Immediate"
    }

    result = engine.evaluate_candidate(
        "Data Scientist",
        ats_result,
        candidate
    )

    assert result["eligibility"] == "REJECTED"


def test_mandatory_skill_failure():

    engine = EligibilityDecisionEngine()

    ats_result = {
        "overall_score": 90
    }

    candidate = {
        "candidate_id": "ELG004",
        "name": "Missing Skills",
        "skills": [
            "Python"
        ],
        "experience_years": 2,
        "location": "Remote",
        "availability": "Immediate"
    }

    result = engine.evaluate_candidate(
        "Data Scientist",
        ats_result,
        candidate
    )

    assert result["eligibility"] == "REVIEW"
    assert "sql" in result[
        "rule_results"
    ]["mandatory_skills"]["missing_skills"]


def test_experience_range():

    engine = EligibilityDecisionEngine()

    ats_result = {
        "overall_score": 90
    }

    candidate = {
        "candidate_id": "ELG005",
        "name": "Experience Test",
        "skills": [
            "Python",
            "SQL"
        ],
        "experience_years": 2,
        "location": "Remote",
        "availability": "Immediate"
    }

    result = engine.evaluate_candidate(
        "Data Scientist",
        ats_result,
        candidate
    )

    assert result[
        "rule_results"
    ]["experience"]["passed"] is True


def test_ats_api_style_output():

    engine = EligibilityDecisionEngine()

    ats_result = {
        "success": True,
        "message": "Candidate scoring completed.",
        "data": {
            "job_role": "Data Scientist",
            "overall_score": 88.0
        }
    }

    candidate = {
        "candidate_id": "ELG006",
        "name": "API Candidate",
        "skills": [
            "Python",
            "SQL"
        ],
        "experience_years": 3
    }

    result = engine.evaluate_candidate(
        "Data Scientist",
        ats_result,
        candidate
    )

    assert result["ats_score"] == 88.0
    assert result["eligibility"] == "ELIGIBLE"


def run_tests():

    test_eligible_candidate()
    test_review_candidate()
    test_rejected_candidate()
    test_mandatory_skill_failure()
    test_experience_range()
    test_ats_api_style_output()

    print()
    print("===== Day 21 Eligibility Decision Engine =====")
    print()
    print("Eligible candidate test: PASSED")
    print("Review candidate test: PASSED")
    print("Rejected candidate test: PASSED")
    print("Mandatory skill validation: PASSED")
    print("Experience range validation: PASSED")
    print("ATS output integration: PASSED")
    print()
    print(
        "All Day 21 Eligibility Decision Engine "
        "tests passed successfully!"
    )


if __name__ == "__main__":
    run_tests()
