"""
Unit Test for ATS REST API

Tests:
- Health endpoint
- Resume parsing contract
- ATS scoring endpoint
- Candidate shortlisting endpoint
- Validation handling
- Job-not-found handling
"""

import json

from fastapi.testclient import TestClient

from ats_engine.api import app


client = TestClient(app)


# ---------------------------------------------------------
# Health Endpoint Test
# ---------------------------------------------------------

def test_health_endpoint():

    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


# ---------------------------------------------------------
# Resume Parsing Endpoint Test
# ---------------------------------------------------------

def test_resume_parsing_endpoint():

    response = client.post(
        "/api/v1/resumes/parse",
        json={
            "resume_text": (
                "Data Scientist with Python, SQL "
                "and Machine Learning experience."
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["status"] == "parsed"


# ---------------------------------------------------------
# ATS Scoring Endpoint Test
# ---------------------------------------------------------

def test_scoring_endpoint():

    response = client.post(
        "/api/v1/scoring",
        json={
            "job_role": "Data Scientist",
            "scores": {
                "skill_match": 90,
                "experience_relevance": 80,
                "education_alignment": 75,
                "semantic_similarity": 85
            }
        }
    )

    # Diagnostic output
    # This will show us the actual API response if
    # the scoring integration fails.

    print(
        "\n===== Scoring API Response =====\n"
    )

    print(
        "Status Code:",
        response.status_code
    )

    try:

        print(
            json.dumps(
                response.json(),
                indent=4
            )
        )

    except Exception:

        print(response.text)

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    assert (
        data["data"]["job_role"]
        == "Data Scientist"
    )

    assert (
        data["data"]["overall_score"]
        > 0
    )


# ---------------------------------------------------------
# Candidate Shortlisting Endpoint Test
# ---------------------------------------------------------

def test_shortlisting_endpoint():

    response = client.post(
        "/api/v1/shortlisting",
        json={
            "candidates": [
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
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True

    result = data["data"]

    assert result["total_candidates"] == 3

    assert (
        result["shortlisted_count"]
        == 1
    )

    assert (
        result["review_count"]
        == 1
    )

    assert (
        result["rejected_count"]
        == 1
    )


# ---------------------------------------------------------
# Validation Error Test
# ---------------------------------------------------------

def test_validation_error():

    response = client.post(
        "/api/v1/scoring",
        json={
            "job_role": "Data Scientist",
            "scores": {
                "skill_match": 150,
                "experience_relevance": 80,
                "education_alignment": 75,
                "semantic_similarity": 85
            }
        }
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Job Not Found Test
# ---------------------------------------------------------

def test_job_not_found():

    response = client.get(
        "/api/v1/jobs/non-existing-job"
    )

    assert response.status_code == 404

    data = response.json()

    assert (
        data["detail"]["success"]
        is False
    )

    assert (
        data["detail"]["error"]["code"]
        == "RESOURCE_NOT_FOUND"
    )


# ---------------------------------------------------------
# Run All API Tests
# ---------------------------------------------------------

def run_api_tests():

    print(
        "\n===== Day 16 ATS API Tests =====\n"
    )

    test_health_endpoint()

    print(
        "Health endpoint test passed."
    )

    test_resume_parsing_endpoint()

    print(
        "Resume parsing API test passed."
    )

    test_scoring_endpoint()

    print(
        "ATS scoring API test passed."
    )

    test_shortlisting_endpoint()

    print(
        "Candidate shortlisting API test passed."
    )

    test_validation_error()

    print(
        "Validation handling test passed."
    )

    test_job_not_found()

    print(
        "Job error handling test passed."
    )

    print(
        "\nAll ATS API Design and "
        "Integration tests passed successfully!"
    )


if __name__ == "__main__":

    run_api_tests()