from scoring.screening_scoring_engine import ScreeningScoringEngine


def test_configuration_file_exists():
    engine = ScreeningScoringEngine()
    assert engine.config_path.exists()


def test_score_normalization():
    engine = ScreeningScoringEngine()

    assert engine._normalize_score(0) == 0
    assert engine._normalize_score(5) == 50
    assert engine._normalize_score(10) == 100


def test_score_is_clamped():
    engine = ScreeningScoringEngine()

    assert engine._normalize_score(-5) == 0
    assert engine._normalize_score(15) == 100


def test_question_scoring():
    engine = ScreeningScoringEngine()

    result = engine.score_question(
        question_id="Q1",
        clarity=8,
        relevance=9,
        completeness=7,
        consistency=8
    )

    assert result["question_id"] == "Q1"
    assert "criteria_scores" in result
    assert "normalized_score" in result
    assert "score_explanation" in result


def test_question_score_calculation():
    engine = ScreeningScoringEngine()

    result = engine.score_question(
        question_id="Q1",
        clarity=10,
        relevance=10,
        completeness=10,
        consistency=10
    )

    assert result["normalized_score"] == 100


def test_multiple_question_scoring():
    engine = ScreeningScoringEngine()

    responses = [
        {
            "question_id": "Q1",
            "clarity": 8,
            "relevance": 9,
            "completeness": 8,
            "consistency": 9
        },
        {
            "question_id": "Q2",
            "clarity": 7,
            "relevance": 8,
            "completeness": 7,
            "consistency": 8
        }
    ]

    result = engine.score_screening(responses)

    assert result["total_questions"] == 2
    assert len(result["question_scores"]) == 2
    assert "final_screening_score" in result
    assert "explanation" in result


def test_perfect_screening_score():
    engine = ScreeningScoringEngine()

    responses = [
        {
            "question_id": "Q1",
            "clarity": 10,
            "relevance": 10,
            "completeness": 10,
            "consistency": 10
        },
        {
            "question_id": "Q2",
            "clarity": 10,
            "relevance": 10,
            "completeness": 10,
            "consistency": 10
        }
    ]

    result = engine.score_screening(responses)

    assert result["final_screening_score"] == 100


def test_empty_screening():
    engine = ScreeningScoringEngine()

    result = engine.score_screening([])

    assert result["total_questions"] == 0
    assert result["final_screening_score"] == 0.0
    assert result["question_scores"] == []


def test_explainable_output():
    engine = ScreeningScoringEngine()

    result = engine.score_question(
        question_id="Q1",
        clarity=8,
        relevance=8,
        completeness=8,
        consistency=8
    )

    explanation = result["score_explanation"]

    assert "clarity_weight" in explanation
    assert "relevance_weight" in explanation
    assert "completeness_weight" in explanation
    assert "consistency_weight" in explanation
