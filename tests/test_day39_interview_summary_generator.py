from scoring.interview_summary_generator import (
    InterviewSummaryGenerator,
)


def sample_interview_evaluation():
    return {
        "interview_score": 84.0,
        "interview_level": "excellent",
        "answer_count": 3,
        "score_breakdown": {
            "answer_relevance": 88.0,
            "communication": 90.0,
            "confidence": 82.0,
            "consistency": 78.0,
        },
    }


def sample_aptitude_evaluation():
    return {
        "aptitude_score": 86.0,
        "aptitude_level": "excellent",
    }


def sample_answers():
    return [
        {
            "question": "Tell me about teamwork.",
            "answer": (
                "I collaborate with my team, communicate clearly, "
                "take ownership, and learn from feedback."
            ),
        },
        {
            "question": "How would you solve a project issue?",
            "answer": (
                "First I identify the cause, then compare options "
                "and communicate the solution to the team."
            ),
        },
        {
            "question": "How do you handle feedback?",
            "answer": (
                "I consider feedback carefully, adapt my approach, "
                "and improve the final result."
            ),
        },
    ]


def test_configuration_and_template_exist():
    generator = InterviewSummaryGenerator()

    assert generator.CONFIG_PATH.exists()
    assert generator.TEMPLATE_PATH.exists()


def test_generator_initialization():
    generator = InterviewSummaryGenerator()

    assert generator.config is not None
    assert generator.template is not None


def test_strength_detection():
    generator = InterviewSummaryGenerator()

    strengths = generator.identify_strengths(
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    assert "Strong overall HR interview performance" in strengths
    assert "Strong communication skills" in strengths
    assert "Strong logical and problem-solving ability" in strengths


def test_weakness_detection():
    generator = InterviewSummaryGenerator()

    evaluation = sample_interview_evaluation()

    evaluation["score_breakdown"]["communication"] = 60.0

    weaknesses = generator.identify_weaknesses(
        evaluation,
        sample_aptitude_evaluation(),
    )

    assert "Communication could be improved" in weaknesses


def test_cultural_fit_detection():
    generator = InterviewSummaryGenerator()

    result = generator.identify_cultural_fit_indicators(
        sample_answers()
    )

    assert "collaborate" in result
    assert "communicate" in result
    assert "ownership" in result
    assert "feedback" in result


def test_risk_detection_low_confidence():
    generator = InterviewSummaryGenerator()

    evaluation = sample_interview_evaluation()

    evaluation["score_breakdown"]["confidence"] = 40.0

    risks = generator.identify_risk_flags(
        evaluation,
        sample_answers(),
        sample_aptitude_evaluation(),
    )

    assert "Low confidence indicators" in risks


def test_risk_detection_risky_language():
    generator = InterviewSummaryGenerator()

    answers = [
        {
            "answer": (
                "I avoid conflict and sometimes refuse to "
                "communicate when there is pressure."
            )
        }
    ]

    risks = generator.identify_risk_flags(
        sample_interview_evaluation(),
        answers,
        sample_aptitude_evaluation(),
    )

    assert any(
        risk.startswith(
            "Potential risk indicator:"
        )
        for risk in risks
    )


def test_inconsistency_detection():
    generator = InterviewSummaryGenerator()

    evaluation = sample_interview_evaluation()

    evaluation["score_breakdown"]["consistency"] = 30.0

    result = generator.identify_inconsistencies(
        evaluation
    )

    assert len(result) == 1
    assert "inconsistency" in result[0].lower()


def test_overall_performance():
    generator = InterviewSummaryGenerator()

    result = generator.summarize_overall_performance(
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    assert result == "Excellent overall HR performance"


def test_natural_language_summary():
    generator = InterviewSummaryGenerator()

    strengths = generator.identify_strengths(
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    weaknesses = generator.identify_weaknesses(
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    risks = generator.identify_risk_flags(
        sample_interview_evaluation(),
        sample_answers(),
        sample_aptitude_evaluation(),
    )

    result = generator.generate_natural_language_summary(
        "Test Candidate",
        sample_interview_evaluation(),
        strengths,
        weaknesses,
        risks,
        sample_aptitude_evaluation(),
    )

    assert "Test Candidate" in result
    assert "84.00" in result
    assert "86.00" in result


def test_recommendation():
    generator = InterviewSummaryGenerator()

    result = generator.determine_recommendation(
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    assert result == "Strongly Recommended"


def test_complete_report_generation():
    generator = InterviewSummaryGenerator()

    report = generator.generate_report(
        candidate_name="Test Candidate",
        job_role="Data Analyst",
        answers=sample_answers(),
        interview_evaluation=sample_interview_evaluation(),
        aptitude_evaluation=sample_aptitude_evaluation(),
    )

    assert report["report_type"] == (
        "AI Interview Summary Report"
    )

    assert report["candidate"]["name"] == (
        "Test Candidate"
    )

    assert report["candidate"]["role"] == (
        "Data Analyst"
    )

    assert "summary" in report
    assert "evaluation" in report
    assert "insights" in report
    assert "recommendation" in report


def test_required_summary_sections():
    generator = InterviewSummaryGenerator()

    report = generator.generate_report(
        "Test Candidate",
        "Data Analyst",
        sample_answers(),
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    insights = report["insights"]

    assert "strengths" in insights
    assert "weaknesses" in insights
    assert "cultural_fit_indicators" in insights
    assert "risk_flags" in insights
    assert "inconsistencies" in insights


def test_text_report_generation():
    generator = InterviewSummaryGenerator()

    report = generator.generate_report(
        "Test Candidate",
        "Data Analyst",
        sample_answers(),
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    text = generator.generate_text_report(report)

    assert "AI INTERVIEW SUMMARY REPORT" in text
    assert "Test Candidate" in text
    assert "Data Analyst" in text
    assert "Strongly Recommended" in text
    assert "STRENGTHS" in text
    assert "WEAKNESSES" in text
    assert "RISK FLAGS" in text


def test_empty_answers():
    generator = InterviewSummaryGenerator()

    report = generator.generate_report(
        "Test Candidate",
        "Data Analyst",
        [],
        sample_interview_evaluation(),
        sample_aptitude_evaluation(),
    )

    assert report["insights"]["cultural_fit_indicators"] == []


def test_invalid_answers_type():
    generator = InterviewSummaryGenerator()

    try:
        generator.generate_report(
            "Test Candidate",
            "Data Analyst",
            "invalid",
            sample_interview_evaluation(),
            sample_aptitude_evaluation(),
        )
        assert False
    except TypeError:
        assert True


def test_invalid_interview_evaluation_type():
    generator = InterviewSummaryGenerator()

    try:
        generator.generate_report(
            "Test Candidate",
            "Data Analyst",
            [],
            "invalid",
            sample_aptitude_evaluation(),
        )
        assert False
    except TypeError:
        assert True
