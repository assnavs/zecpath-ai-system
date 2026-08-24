from interview_ai.interview import InterviewAI


def test_interview_initialization():
    interview = InterviewAI(
        "Data Scientist",
        "fresher",
    )

    state = interview.get_interview_state()

    assert state["role"] == "Data Scientist"
    assert state["experience_level"] == "fresher"
    assert state["phase"] == "introduction"
    assert state["completed"] is False


def test_hr_categories():
    interview = InterviewAI(
        "Data Scientist"
    )

    categories = interview.get_hr_categories()

    assert "Self-introduction" in categories
    assert "Career journey" in categories
    assert "Strengths & weaknesses" in categories
    assert "Teamwork & culture fit" in categories
    assert "Career goals" in categories
    assert "Availability & commitment" in categories


def test_conversation_phases():
    interview = InterviewAI(
        "Data Scientist"
    )

    phases = interview.get_conversation_phases()

    assert phases == [
        "introduction",
        "core_hr_questions",
        "role_based_evaluation",
        "closing",
    ]


def test_technical_role_detection():
    technical = InterviewAI(
        "Data Scientist"
    )

    assert technical.get_role_type() == "technical"


def test_non_technical_role_detection():
    non_technical = InterviewAI(
        "HR Coordinator"
    )

    assert non_technical.get_role_type() == "non_technical"


def test_role_based_question_generation():
    interview = InterviewAI(
        "Data Scientist",
        "experienced",
    )

    questions = interview.generate_questions()

    assert len(questions) == 7

    for question in questions:
        assert question["role"] == "Data Scientist"
        assert question["role_type"] == "technical"
        assert question["experience_level"] == "experienced"


def test_start_interview():
    interview = InterviewAI(
        "Data Analyst"
    )

    result = interview.start_interview()

    assert result["phase"] == "introduction"
    assert result["question"] is not None
    assert result["question"]["category"] == "Introduction"
    assert result["state"]["question_id"] is not None


def test_response_capture():
    interview = InterviewAI(
        "Data Scientist"
    )

    interview.start_interview()

    state = interview.capture_response(
        "Python and machine learning."
    )

    assert state["response_received"] is True
    assert state["response"] == (
        "Python and machine learning."
    )


def test_short_response_follow_up():
    interview = InterviewAI(
        "Data Scientist"
    )

    interview.start_interview()

    state = interview.capture_response(
        "Python."
    )

    assert state["response_received"] is True
    assert state["follow_up_eligible"] is True


def test_detailed_response_no_follow_up():
    interview = InterviewAI(
        "Data Scientist"
    )

    interview.start_interview()

    state = interview.capture_response(
        "I have worked with Python, SQL, "
        "machine learning and data visualization "
        "through several academic and practical projects."
    )

    assert state["response_received"] is True
    assert state["follow_up_eligible"] is False


def test_phase_transition():
    interview = InterviewAI(
        "Data Scientist"
    )

    result = interview.move_to_phase(
        "core_hr_questions"
    )

    assert result["phase"] == "core_hr_questions"
    assert result["question"] is not None


def test_role_based_phase():
    interview = InterviewAI(
        "Software Engineer"
    )

    result = interview.move_to_phase(
        "role_based_evaluation"
    )

    assert result["phase"] == "role_based_evaluation"
    assert result["question"] is not None
    assert result["question"]["category"] == "Skills"


def test_closing_phase():
    interview = InterviewAI(
        "Data Scientist"
    )

    result = interview.move_to_phase(
        "closing"
    )

    assert result["phase"] == "closing"
    assert result["completed"] is True
