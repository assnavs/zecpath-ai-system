from scoring.confidence_sentiment_engine import ConfidenceSentimentEngine


def test_configuration_file_exists():
    engine = ConfidenceSentimentEngine()

    assert engine.config_path.exists()


def test_empty_response():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response("")

    assert "confidence_score" in result
    assert "communication_strength" in result
    assert "signals" in result


def test_hesitation_detection():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "Um, I have experience in Python and SQL."
    )

    assert result["signals"]["hesitation"]["hesitation_count"] > 0


def test_uncertainty_detection():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I think I might be able to work with Python."
    )

    assert result["signals"]["uncertainty"]["uncertainty_count"] > 0


def test_positive_sentiment_detection():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I successfully completed an excellent Python project."
    )

    assert result["signals"]["sentiment"]["sentiment"] == "positive"


def test_negative_sentiment_detection():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I was confused and unable to complete the task."
    )

    assert result["signals"]["sentiment"]["sentiment"] == "negative"


def test_response_length_signal():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I have experience working with Python, SQL, "
        "Power BI, and machine learning projects."
    )

    assert "response_length" in result["signals"]


def test_confidence_score_range():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I am confident and experienced in Python and SQL."
    )

    assert 0 <= result["confidence_score"] <= 100


def test_communication_strength_classification():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I successfully completed several projects "
        "and I am confident in my technical skills."
    )

    assert result["communication_strength"] in [
        "strong",
        "moderate",
        "needs_improvement"
    ]


def test_consistency_signal():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I have experience in Python and Python development.",
        previous_answer="I have experience in Python."
    )

    assert "consistency" in result["signals"]


def test_pace_analysis():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I have experience in Python and SQL.",
        duration_seconds=3
    )

    assert result["signals"]["pace"]["pace_available"] is True
    assert result["signals"]["pace"]["words_per_second"] is not None


def test_structured_output():
    engine = ConfidenceSentimentEngine()

    result = engine.analyze_response(
        "I am confident and experienced in Python."
    )

    assert "raw_text" in result
    assert "normalized_text" in result
    assert "confidence_score" in result
    assert "communication_strength" in result
    assert "signals" in result

    assert "hesitation" in result["signals"]
    assert "response_length" in result["signals"]
    assert "pace" in result["signals"]
    assert "sentiment" in result["signals"]
    assert "uncertainty" in result["signals"]
    assert "consistency" in result["signals"]
