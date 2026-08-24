from interview_ai.follow_up_engine import DynamicFollowUpEngine


def test_empty_response_triggers_clarification():
    engine = DynamicFollowUpEngine()

    result = engine.analyze_response("")

    assert result["follow_up_eligible"] is True
    assert result["trigger"] == "clarification"
    assert result["reason"] == "empty_response"


def test_vague_response_triggers_clarification():
    engine = DynamicFollowUpEngine()

    result = engine.analyze_response("Yes")

    assert result["follow_up_eligible"] is True
    assert result["trigger"] == "clarification"
    assert result["reason"] == "vague_response"
    assert result["follow_up"]["type"] == "clarification"


def test_very_short_response_triggers_clarification():
    engine = DynamicFollowUpEngine()

    result = engine.analyze_response("Python.")

    assert result["follow_up_eligible"] is True
    assert result["trigger"] == "clarification"
    assert result["reason"] == "very_short_response"


def test_short_response_triggers_deepening():
    engine = DynamicFollowUpEngine()

    result = engine.analyze_response("Python and SQL.")

    assert result["follow_up_eligible"] is True
    assert result["trigger"] == "deepening"
    assert result["reason"] == "short_response"


def test_confident_response_triggers_scenario():
    engine = DynamicFollowUpEngine()

    result = engine.analyze_response(
        "I developed a machine learning model."
    )

    assert result["follow_up_eligible"] is True
    assert result["trigger"] == "scenario"
    assert result["reason"] == "confident_response"


def test_detailed_response_triggers_example():
    engine = DynamicFollowUpEngine()

    result = engine.analyze_response(
        "I worked on several projects involving Python, "
        "SQL, machine learning, data analysis and "
        "visualization for academic and practical work."
    )

    assert result["follow_up_eligible"] is True
    assert result["trigger"] == "example"
    assert result["reason"] == "detailed_response"


def test_maximum_follow_ups_are_limited():
    engine = DynamicFollowUpEngine()

    first = engine.analyze_response("Yes")
    second = engine.analyze_response("Python and SQL.")
    third = engine.analyze_response("Yes")

    assert first["follow_up_eligible"] is True
    assert second["follow_up_eligible"] is True
    assert third["follow_up_eligible"] is False
    assert third["reason"] == "maximum_follow_ups_reached"
    assert engine.get_state()["follow_up_count"] == 2


def test_follow_up_questions_are_not_repeated():
    engine = DynamicFollowUpEngine()

    first = engine.analyze_response("Yes")
    second = engine.analyze_response("Yes")

    assert first["follow_up"]["text"] == (
        "Could you please provide a little more detail?"
    )

    assert second["follow_up"] is None


def test_reset_clears_follow_up_state():
    engine = DynamicFollowUpEngine()

    engine.analyze_response("Yes")
    engine.reset()

    state = engine.get_state()

    assert state["follow_up_count"] == 0
    assert state["follow_up_eligible"] is False
    assert state["last_trigger"] is None
    assert state["asked_follow_ups"] == []


def test_should_continue_for_sufficient_response():
    engine = DynamicFollowUpEngine()

    result = engine.should_continue(
        "I have experience working with Python, SQL, "
        "machine learning and data visualization."
    )

    assert result is True


def test_should_not_continue_for_incomplete_response():
    engine = DynamicFollowUpEngine()

    result = engine.should_continue("Yes")

    assert result is False
