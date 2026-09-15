from scoring.aptitude_logic_engine import (
    AptitudeLogicEngine,
)


def test_configuration_file_exists():
    engine = AptitudeLogicEngine()

    assert engine.CONFIG_PATH.exists()


def test_engine_initialization():
    engine = AptitudeLogicEngine()

    assert engine.config is not None
    assert "weights" in engine.config
    assert "thresholds" in engine.config


def test_empty_answer_problem_understanding():
    engine = AptitudeLogicEngine()

    score = engine.calculate_problem_understanding(
        "",
        ["deadline", "priority"],
    )

    assert score == 0.0


def test_problem_understanding_with_matching_keywords():
    engine = AptitudeLogicEngine()

    score = engine.calculate_problem_understanding(
        "I would prioritize the deadline and review the priority.",
        ["deadline", "priority"],
    )

    assert score == 100.0


def test_problem_understanding_partial_match():
    engine = AptitudeLogicEngine()

    score = engine.calculate_problem_understanding(
        "I would check the deadline.",
        ["deadline", "priority"],
    )

    assert score == 50.0


def test_logical_reasoning_empty_answer():
    engine = AptitudeLogicEngine()

    assert (
        engine.calculate_logical_reasoning("")
        == 0.0
    )


def test_logical_reasoning_structured_answer():
    engine = AptitudeLogicEngine()

    score = engine.calculate_logical_reasoning(
        "First I identify the cause, then I compare the options, "
        "and finally I evaluate the impact before deciding."
    )

    assert score > 40.0
    assert score <= 100.0


def test_decision_quality_with_expected_actions():
    engine = AptitudeLogicEngine()

    score = engine.calculate_decision_quality(
        "I would analyze the issue, communicate with the team, "
        "and create a plan to resolve it.",
        [
            "analyze",
            "communicate",
            "plan",
        ],
    )

    assert score == 100.0


def test_problem_solving_clarity():
    engine = AptitudeLogicEngine()

    score = engine.calculate_problem_solving_clarity(
        "First I identify the problem. Then I analyze the cause "
        "and create a solution plan. Finally I test and verify it."
    )

    assert score > 50.0
    assert score <= 100.0


def test_reasoning_evaluation():
    engine = AptitudeLogicEngine()

    result = engine.evaluate_reasoning(
        answer=(
            "First I identify the issue, then analyze the options "
            "and communicate the plan before implementing the solution."
        ),
        expected_keywords=[
            "issue",
            "options",
            "plan",
        ],
        expected_actions=[
            "analyze",
            "communicate",
            "implement",
        ],
    )

    assert "scores" in result
    assert "aptitude_score" in result
    assert "aptitude_level" in result

    assert 0 <= result["aptitude_score"] <= 100


def test_scenario_evaluation():
    engine = AptitudeLogicEngine()

    scenario = {
        "scenario": (
            "A project deadline is approaching and an important "
            "task is incomplete."
        ),
        "expected_keywords": [
            "deadline",
            "task",
        ],
        "expected_actions": [
            "prioritize",
            "communicate",
            "plan",
        ],
    }

    result = engine.evaluate_scenario(
        scenario,
        "I would prioritize the task, communicate the risk, "
        "and create a plan to meet the deadline.",
    )

    assert result["scenario"] == scenario["scenario"]
    assert "evaluation" in result
    assert "aptitude_score" in result["evaluation"]


def test_invalid_scenario():
    engine = AptitudeLogicEngine()

    try:
        engine.evaluate_scenario(
            {"expected_keywords": ["problem"]},
            "I would analyze the problem.",
        )
        assert False
    except ValueError:
        assert True


def test_multiple_response_evaluation():
    engine = AptitudeLogicEngine()

    responses = [
        {
            "answer": (
                "First I identify the issue, then analyze the cause "
                "and create a solution plan."
            ),
            "expected_keywords": [
                "issue",
                "cause",
                "solution",
            ],
            "expected_actions": [
                "analyze",
                "plan",
            ],
        },
        {
            "answer": (
                "I would compare the options and choose the approach "
                "that reduces the impact."
            ),
            "expected_keywords": [
                "options",
                "impact",
            ],
            "expected_actions": [
                "compare",
            ],
        },
    ]

    result = engine.evaluate_interview(responses)

    assert result["response_count"] == 2
    assert 0 <= result["aptitude_score"] <= 100
    assert len(result["response_results"]) == 2
    assert "score_breakdown" in result


def test_empty_interview():
    engine = AptitudeLogicEngine()

    result = engine.evaluate_interview([])

    assert result["aptitude_score"] == 0.0
    assert result["response_count"] == 0
    assert result["response_results"] == []


def test_invalid_responses_type():
    engine = AptitudeLogicEngine()

    try:
        engine.evaluate_interview("invalid")
        assert False
    except TypeError:
        assert True


def test_missing_answer_field():
    engine = AptitudeLogicEngine()

    try:
        engine.evaluate_interview(
            [{"expected_keywords": ["problem"]}]
        )
        assert False
    except ValueError:
        assert True


def test_score_classification():
    engine = AptitudeLogicEngine()

    assert engine.classify_score(90) == "excellent"
    assert engine.classify_score(70) == "good"
    assert engine.classify_score(55) == "moderate"
    assert (
        engine.classify_score(30)
        == "needs_improvement"
    )


def test_aptitude_report():
    engine = AptitudeLogicEngine()

    responses = [
        {
            "answer": (
                "First I identify the problem, analyze the cause, "
                "and create a solution plan."
            ),
            "expected_keywords": [
                "problem",
                "cause",
                "solution",
            ],
            "expected_actions": [
                "analyze",
                "plan",
            ],
        }
    ]

    report = engine.generate_aptitude_report(
        responses
    )

    assert "candidate_aptitude_report" in report

    candidate_report = (
        report["candidate_aptitude_report"]
    )

    assert "aptitude_score" in candidate_report
    assert "aptitude_level" in candidate_report
    assert "response_count" in candidate_report
    assert "score_breakdown" in candidate_report
    assert "response_results" in candidate_report
