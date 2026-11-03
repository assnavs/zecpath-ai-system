import pytest

from interview_ai.technical_interview_engine import (
    TechnicalInterviewEngine,
)


@pytest.mark.parametrize(
    "years,expected",
    [
        (0, "entry"),
        (2, "entry"),
        (3, "intermediate"),
        (4.9, "intermediate"),
        (5, "advanced"),
        (8, "advanced"),
    ],
)
def test_experience_level_mapping(years, expected):
    engine = TechnicalInterviewEngine("MERN Developer", years)
    assert engine.experience_level == expected


@pytest.mark.parametrize(
    "role,expected_skills",
    [
        (
            "MERN Developer",
            ["MongoDB", "Express.js", "React", "Node.js", "JavaScript"],
        ),
        (
            "Java Developer",
            ["Java", "OOP", "Spring Boot", "SQL", "REST APIs"],
        ),
        (
            "DevOps Engineer",
            ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Monitoring"],
        ),
    ],
)
def test_role_skill_mapping(role, expected_skills):
    engine = TechnicalInterviewEngine(role, 2)
    assert engine.get_role_skills() == expected_skills


def test_interview_structure():
    engine = TechnicalInterviewEngine("MERN Developer", 2)
    assert engine.get_interview_structure() == [
        "introduction",
        "experience_based",
        "conceptual",
        "scenario_based",
    ]


def test_start_interview():
    engine = TechnicalInterviewEngine("MERN Developer", 2)
    result = engine.start_interview()

    assert result["state"] == "introduction"
    assert result["experience_level"] == "entry"
    assert result["question_count"] == 3
    assert result["question"]["difficulty"] == "basic"


def test_questions_match_experience_level():
    engine = TechnicalInterviewEngine("Java Developer", 4)

    for question in engine.get_questions():
        assert question["experience_level"] == "intermediate"
        assert question["difficulty"] == "intermediate"


def test_submit_response():
    engine = TechnicalInterviewEngine("DevOps Engineer", 2)
    engine.start_interview()

    result = engine.submit_response("Docker packages applications.")

    assert result["submitted"] is True
    assert result["response_count"] == 1
    assert result["next_question"] is not None


def test_evaluation_input():
    engine = TechnicalInterviewEngine("MERN Developer", 2)
    engine.start_interview()
    engine.submit_response("JavaScript supports multiple programming patterns.")

    result = engine.generate_evaluation_input()

    assert result["role"] == "MERN Developer"
    assert len(result["responses"]) == 1
    assert result["responses"][0]["skill"] == "JavaScript"


def test_flow_transitions():
    engine = TechnicalInterviewEngine("Java Developer", 2)

    expected_states = [
        "experience_based",
        "conceptual",
        "scenario_based",
        "evaluation",
        "closing",
        "completed",
    ]

    for expected in expected_states:
        if engine.current_state == "scenario_based":
            for _ in range(len(engine.questions) - engine.current_question_index):
                engine.submit_response("Sample technical interview answer.")

        result = engine.advance_flow()
        assert result["state"] == expected


def test_scenario_transition_requires_all_questions():
    engine = TechnicalInterviewEngine("MERN Developer", 2)

    engine.advance_flow()
    engine.advance_flow()
    engine.advance_flow()

    with pytest.raises(RuntimeError):
        engine.advance_flow()


def test_invalid_role():
    with pytest.raises(ValueError):
        TechnicalInterviewEngine("Unknown Developer", 2)


def test_negative_experience():
    with pytest.raises(ValueError):
        TechnicalInterviewEngine("MERN Developer", -1)


def test_non_numeric_experience():
    with pytest.raises(TypeError):
        TechnicalInterviewEngine("MERN Developer", "fresher")


def test_non_string_answer():
    engine = TechnicalInterviewEngine("MERN Developer", 2)
    engine.start_interview()

    with pytest.raises(TypeError):
        engine.submit_response(123)


def test_session_reset():
    engine = TechnicalInterviewEngine("MERN Developer", 2)
    engine.start_interview()
    engine.submit_response("My answer.")

    result = engine.start_interview()

    assert result["state"] == "introduction"
    assert result["question_count"] == 3
    assert engine.responses == []
    assert engine.current_question_index == 0
