from screening_ai.answer_intent_engine import AnswerIntentEngine


def test_pattern_file_exists():
    engine = AnswerIntentEngine()

    assert engine.pattern_file.exists()


def test_skills_intent_classification():
    engine = AnswerIntentEngine()

    result = engine.classify_intent(
        "I have skills in Python, SQL and Power BI"
    )

    assert result["intent"] == "skills"


def test_experience_intent_classification():
    engine = AnswerIntentEngine()

    result = engine.classify_intent(
        "I have three years of experience in data analysis"
    )

    assert result["intent"] == "experience"


def test_availability_intent_classification():
    engine = AnswerIntentEngine()

    result = engine.classify_intent(
        "I am available to join immediately"
    )

    assert result["intent"] == "availability"


def test_salary_intent_classification():
    engine = AnswerIntentEngine()

    result = engine.classify_intent(
        "My expected salary is 6 LPA"
    )

    assert result["intent"] == "salary_expectation"


def test_skill_extraction():
    engine = AnswerIntentEngine()

    result = engine.understand(
        "I have experience with Python, SQL and Power BI"
    )

    assert "python" in result["semantic_data"]["skills"]
    assert "sql" in result["semantic_data"]["skills"]
    assert "power bi" in result["semantic_data"]["skills"]


def test_experience_extraction():
    engine = AnswerIntentEngine()

    result = engine.understand(
        "I have 3 years of experience in data analysis"
    )

    assert result["semantic_data"]["experience_details"]["years"] == [3]


def test_salary_extraction():
    engine = AnswerIntentEngine()

    result = engine.understand(
        "I expect around 6 LPA"
    )

    assert 6 in result["semantic_data"]["salary_expectation"]["values"]


def test_off_topic_detection():
    engine = AnswerIntentEngine()

    result = engine.understand(
        "I watched a cricket match yesterday"
    )

    assert result["off_topic"] is True
    assert result["response_status"] == "off_topic"


def test_vague_answer_detection():
    engine = AnswerIntentEngine()

    result = engine.understand("Maybe")

    assert result["missing_or_vague"] is True
    assert result["response_status"] == "missing_or_vague"


def test_structured_semantic_object():
    engine = AnswerIntentEngine()

    result = engine.understand(
        "I have 2 years of experience in Python"
    )

    assert "intent" in result
    assert "confidence" in result
    assert "semantic_data" in result
    assert result["response_status"] == "understood"


def test_empty_answer():
    engine = AnswerIntentEngine()

    result = engine.understand("")

    assert result["intent"] == "unknown"
    assert result["missing_or_vague"] is True


def test_multiple_answer_types():
    engine = AnswerIntentEngine()

    answers = [
        "I know Python and SQL",
        "I have 2 years of experience",
        "I can join immediately",
        "My expected salary is 5 LPA"
    ]

    results = [engine.understand(answer) for answer in answers]

    assert results[0]["intent"] == "skills"
    assert results[1]["intent"] == "experience"
    assert results[2]["intent"] == "availability"
    assert results[3]["intent"] == "salary_expectation"
