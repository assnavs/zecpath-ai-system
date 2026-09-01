from scoring.hr_interview_scoring_engine import (
    HRInterviewScoringEngine,
)


def test_configuration_file_exists():
    engine = HRInterviewScoringEngine()

    assert engine.CONFIG_PATH.exists()


def test_engine_initialization():
    engine = HRInterviewScoringEngine()

    assert engine.config is not None
    assert engine.communication_engine is not None
    assert engine.confidence_engine is not None


def test_relevance_with_matching_keywords():
    engine = HRInterviewScoringEngine()

    score = engine.calculate_relevance(
        "I have worked with Python and SQL projects.",
        ["python", "sql"],
    )

    assert score == 100.0


def test_relevance_with_partial_keywords():
    engine = HRInterviewScoringEngine()

    score = engine.calculate_relevance(
        "I have worked with Python projects.",
        ["python", "sql"],
    )

    assert score == 50.0


def test_empty_answer_relevance():
    engine = HRInterviewScoringEngine()

    score = engine.calculate_relevance(
        "",
        ["python"],
    )

    assert score == 0.0


def test_relevance_without_expected_keywords():
    engine = HRInterviewScoringEngine()

    score = engine.calculate_relevance(
        "I have worked on several projects.",
    )

    assert score == 100.0


def test_first_answer_consistency():
    engine = HRInterviewScoringEngine()

    score = engine.calculate_consistency(
        "I have experience in Python.",
    )

    assert score == 100.0


def test_consistency_between_answers():
    engine = HRInterviewScoringEngine()

    score = engine.calculate_consistency(
        "I have experience in Python development.",
        "I have experience in Python projects.",
    )

    assert 0.0 <= score <= 100.0


def test_score_single_answer():
    engine = HRInterviewScoringEngine()

    result = engine.score_answer(
        answer=(
            "I successfully completed Python and SQL "
            "projects and explained my approach clearly."
        ),
        expected_keywords=[
            "python",
            "sql",
            "projects",
        ],
    )

    assert "weighted_score" in result
    assert "scores" in result

    assert 0 <= result["weighted_score"] <= 100

    assert "answer_relevance" in result["scores"]
    assert "communication" in result["scores"]
    assert "confidence" in result["scores"]
    assert "consistency" in result["scores"]


def test_score_interview():
    engine = HRInterviewScoringEngine()

    answers = [
        {
            "answer": (
                "I have experience working with Python "
                "and SQL for academic projects."
            ),
            "expected_keywords": [
                "python",
                "sql",
            ],
        },
        {
            "answer": (
                "I communicate clearly with my team and "
                "successfully completed project tasks."
            ),
            "expected_keywords": [
                "team",
                "project",
            ],
        },
    ]

    result = engine.score_interview(answers)

    assert result["answer_count"] == 2

    assert 0 <= result["interview_score"] <= 100

    assert "interview_level" in result
    assert "score_breakdown" in result
    assert len(result["answer_results"]) == 2


def test_empty_interview():
    engine = HRInterviewScoringEngine()

    result = engine.score_interview([])

    assert result["interview_score"] == 0.0
    assert result["answer_count"] == 0
    assert result["answer_results"] == []


def test_invalid_answers_type():
    engine = HRInterviewScoringEngine()

    try:
        engine.score_interview("invalid")

        assert False

    except TypeError:
        assert True


def test_missing_answer_field():
    engine = HRInterviewScoringEngine()

    try:
        engine.score_interview(
            [
                {
                    "expected_keywords": [
                        "python",
                    ]
                }
            ]
        )

        assert False

    except ValueError:
        assert True


def test_score_classification():
    engine = HRInterviewScoringEngine()

    assert (
        engine._classify_score(90)
        == "excellent"
    )

    assert (
        engine._classify_score(70)
        == "good"
    )

    assert (
        engine._classify_score(55)
        == "moderate"
    )

    assert (
        engine._classify_score(30)
        == "needs_improvement"
    )


def test_candidate_report():
    engine = HRInterviewScoringEngine()

    answers = [
        {
            "answer": (
                "I am confident in Python and SQL and "
                "have completed several projects."
            ),
            "expected_keywords": [
                "python",
                "sql",
            ],
        }
    ]

    report = engine.generate_candidate_report(
        answers
    )

    assert "candidate_hr_report" in report

    candidate_report = (
        report["candidate_hr_report"]
    )

    assert "interview_score" in candidate_report
    assert "interview_level" in candidate_report
    assert "answer_count" in candidate_report
    assert "score_breakdown" in candidate_report

    assert (
        candidate_report[
            "normalization_method"
        ]
        == "average_per_answer"
    )
