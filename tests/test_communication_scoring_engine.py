from scoring.communication_scoring_engine import (
    CommunicationScoringEngine,
)


def test_engine_initialization():
    engine = CommunicationScoringEngine()

    assert engine is not None


def test_basic_response_analysis():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I have worked on Python and SQL projects."
    )

    assert "communication_score" in result
    assert "communication_level" in result
    assert "metrics" in result


def test_communication_score_range():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I have experience working with Python, SQL, "
        "data analysis and machine learning projects."
    )

    assert 0 <= result["communication_score"] <= 100


def test_fluency_metric():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I enjoy solving problems. "
        "I also like working with data."
    )

    assert "fluency" in result["metrics"]
    assert (
        result["metrics"]["fluency"]["sentence_count"]
        >= 1
    )


def test_grammar_metric():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I have experience with Python and SQL."
    )

    assert "grammar" in result["metrics"]
    assert (
        "grammar_score"
        in result["metrics"]["grammar"]
    )


def test_vocabulary_metric():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I have worked with Python, SQL, machine "
        "learning, analytics and visualization."
    )

    assert "vocabulary" in result["metrics"]
    assert (
        result["metrics"]["vocabulary"]["word_count"]
        > 0
    )


def test_clarity_metric():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I clearly explain my approach when solving problems."
    )

    assert "clarity" in result["metrics"]
    assert (
        "clarity_score"
        in result["metrics"]["clarity"]
    )


def test_filler_detection():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "Um, I have experience with Python and SQL."
    )

    assert "fillers" in result["metrics"]
    assert (
        result["metrics"]["fillers"]["filler_count"]
        >= 1
    )


def test_structure_metric():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I completed several projects. "
        "I learned Python and SQL. "
        "I also worked with data visualization."
    )

    assert "structure" in result["metrics"]
    assert (
        result["metrics"]["structure"]["sentence_count"]
        >= 1
    )


def test_communication_level():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I have worked on Python and SQL projects, "
        "and I enjoy explaining my approach clearly."
    )

    assert result["communication_level"] in {
        "excellent",
        "good",
        "moderate",
        "needs_improvement",
    }


def test_empty_response():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response("")

    assert "communication_score" in result
    assert "metrics" in result


def test_structured_output():
    engine = CommunicationScoringEngine()

    result = engine.analyze_response(
        "I am confident in explaining my technical experience."
    )

    assert "raw_text" in result
    assert "normalized_text" in result
    assert "communication_score" in result
    assert "communication_level" in result
    assert "metrics" in result

    expected_metrics = {
        "fluency",
        "grammar",
        "vocabulary",
        "clarity",
        "fillers",
        "structure",
    }

    assert expected_metrics.issubset(
        result["metrics"].keys()
    )
