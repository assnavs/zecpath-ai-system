import pytest

from interview_ai.follow_up_engine import DynamicFollowUpEngine
from interview_ai.interview import InterviewAI
from scoring.hr_interview_scoring_engine import HRInterviewScoringEngine


def test_duplicate_follow_up_is_not_reported_as_eligible():
    engine = DynamicFollowUpEngine()
    first = engine.analyze_response("Yes")
    second = engine.analyze_response("Yes")

    assert first["follow_up_eligible"] is True
    assert first["follow_up"] is not None
    assert second["follow_up_eligible"] is False
    assert second["follow_up"] is None
    assert second["reason"] == "duplicate_follow_up_suppressed"
    assert engine.get_state()["follow_up_count"] == 1


def test_follow_up_limit_remains_enforced():
    engine = DynamicFollowUpEngine()
    engine.analyze_response("Yes")
    engine.analyze_response("Python and SQL.")
    result = engine.analyze_response("Yes")

    assert result["follow_up_eligible"] is False
    assert result["reason"] == "maximum_follow_ups_reached"
    assert engine.get_state()["follow_up_count"] == 2


def test_interview_response_collapses_internal_whitespace():
    interview = InterviewAI("Data Scientist")
    result = interview.capture_response(
        "  I have  Python\n and   SQL experience.  "
    )

    assert result["response"] == "I have Python and SQL experience."
    assert result["response_received"] is True


def test_blank_interview_response_remains_blank_after_cleanup():
    interview = InterviewAI("Data Scientist")
    result = interview.capture_response("  \n  ")

    assert result["response"] == ""
    assert result["response_received"] is False


def test_hr_scoring_normalizes_answer_whitespace():
    engine = HRInterviewScoringEngine()
    result = engine.score_answer(
        answer="  I have\n Python   and SQL experience. ",
        expected_keywords=["python", "sql"],
    )

    assert result["answer"] == "I have Python and SQL experience."
    assert result["scores"]["answer_relevance"] == 100.0
    assert 0.0 <= result["weighted_score"] <= 100.0


@pytest.mark.parametrize("answer", ["", "   ", "\n\t"])
def test_hr_scoring_handles_blank_answers(answer):
    engine = HRInterviewScoringEngine()
    result = engine.score_answer(
        answer=answer,
        expected_keywords=["python"],
    )

    assert result["answer"] == ""
    assert result["scores"]["answer_relevance"] == 0.0
    assert 0.0 <= result["weighted_score"] <= 100.0
