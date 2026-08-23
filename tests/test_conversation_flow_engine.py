from screening_ai.conversation_flow_engine import ConversationFlowEngine


def test_configuration_file_exists():
    engine = ConversationFlowEngine()

    assert engine.config_path.exists()


def test_initial_state():
    engine = ConversationFlowEngine()

    state = engine.get_state("start")

    assert state["next_state"] == "asking"


def test_state_transition():
    engine = ConversationFlowEngine()

    assert engine.get_next_state("start") == "asking"
    assert engine.get_next_state("asking") == "listening"
    assert engine.get_next_state("listening") == "evaluating"
    assert engine.get_next_state("evaluating") == "decision"


def test_unknown_state():
    engine = ConversationFlowEngine()

    try:
        engine.get_state("unknown_state")
        assert False
    except ValueError:
        assert True


def test_understood_response():
    engine = ConversationFlowEngine()

    result = engine.evaluate_response("understood")

    assert result["action"] == "continue"
    assert result["response_type"] == "understood"


def test_silence_response():
    engine = ConversationFlowEngine()

    result = engine.evaluate_response("silence")

    assert result["action"] == "retry"
    assert result["response_type"] == "silence"
    assert result["message"]


def test_vague_response():
    engine = ConversationFlowEngine()

    result = engine.evaluate_response("missing_or_vague")

    assert result["action"] == "clarify"
    assert result["message"]


def test_off_topic_response():
    engine = ConversationFlowEngine()

    result = engine.evaluate_response("off_topic")

    assert result["action"] == "redirect"


def test_unknown_response():
    engine = ConversationFlowEngine()

    result = engine.evaluate_response("some_unknown_response")

    assert result["action"] == "clarify"
    assert result["response_type"] == "some_unknown_response"


def test_retry_policy():
    engine = ConversationFlowEngine()

    result = engine.handle_retry(0)

    assert result["continue"] is True
    assert result["action"] == "repeat_question"


def test_second_retry_policy():
    engine = ConversationFlowEngine()

    result = engine.handle_retry(1)

    assert result["continue"] is True
    assert result["action"] == "clarify_question"


def test_maximum_retry_policy():
    engine = ConversationFlowEngine()

    result = engine.handle_retry(2)

    assert result["continue"] is False
    assert result["action"] == "continue_with_available_information"


def test_successful_transition():
    engine = ConversationFlowEngine()

    result = engine.transition(
        current_state="listening",
        response_type="understood"
    )

    assert result["current_state"] == "listening"
    assert result["next_state"] == "evaluating"
    assert result["action"] == "continue"
    assert result["continue"] is True


def test_silence_transition():
    engine = ConversationFlowEngine()

    result = engine.transition(
        current_state="listening",
        response_type="silence",
        retry_count=0
    )

    assert result["current_state"] == "listening"
    assert result["next_state"] == "listening"
    assert result["action"] == "repeat_question"
    assert result["continue"] is True


def test_maximum_retry_transition():
    engine = ConversationFlowEngine()

    result = engine.transition(
        current_state="listening",
        response_type="silence",
        retry_count=2
    )

    assert result["action"] == "continue_with_available_information"
    assert result["continue"] is False


def test_clarification_transition():
    engine = ConversationFlowEngine()

    result = engine.transition(
        current_state="evaluating",
        response_type="missing_or_vague"
    )

    assert result["current_state"] == "evaluating"
    assert result["next_state"] == "evaluating"
    assert result["action"] == "clarify"
    assert result["continue"] is True


def test_interrupted_response():
    engine = ConversationFlowEngine()

    result = engine.evaluate_response("interrupted")

    assert result["action"] == "retry"
    assert result["message"]


def test_complete_flow():
    engine = ConversationFlowEngine()

    flow = engine.get_flow()

    assert "states" in flow
    assert "response_rules" in flow
    assert "retry_policy" in flow


def test_completed_state():
    engine = ConversationFlowEngine()

    result = engine.transition(
        current_state="completed",
        response_type="understood"
    )

    assert result["current_state"] == "completed"
    assert result["next_state"] is None
    assert result["continue"] is False
