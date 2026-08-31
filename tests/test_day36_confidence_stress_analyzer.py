from scoring.confidence_stress_analyzer import (
    ConfidenceStressAnalyzer,
)


def test_analyzer_initialization():
    analyzer = ConfidenceStressAnalyzer()

    assert analyzer.confidence_engine is not None


def test_long_pause_detection():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_long_pauses(
        "I worked on Python... and SQL."
    )

    assert result["pause_count"] > 0
    assert result["ellipsis_count"] > 0


def test_dash_pause_detection():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_long_pauses(
        "I have experience -- mainly in Python."
    )

    assert result["dash_pause_count"] > 0


def test_repeated_word_detection():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_repeated_words(
        "I I worked on a project."
    )

    assert result["repetition_count"] == 1
    assert "i" in result["repeated_words"]


def test_no_repeated_words():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_repeated_words(
        "I worked on Python and SQL projects."
    )

    assert result["repetition_count"] == 0


def test_stress_detection():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_stress(
        "I was nervous and worried during the interview."
    )

    assert result["stress_count"] >= 2
    assert result["stress_level"] == "moderate"


def test_low_stress_response():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_stress(
        "I am comfortable explaining my project work."
    )

    assert result["stress_count"] == 0
    assert result["stress_level"] == "low"


def test_behavioral_confidence_score_range():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_response(
        "I successfully completed several Python "
        "and SQL projects and confidently explained "
        "my approach."
    )

    assert (
        0
        <= result["behavioral_confidence_score"]
        <= 100
    )


def test_behavioral_confidence_level():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_response(
        "I successfully completed several projects "
        "and I am confident and comfortable explaining "
        "my technical approach."
    )

    assert result[
        "behavioral_confidence_level"
    ] in {
        "strong",
        "moderate",
        "needs_improvement",
    }


def test_complete_structured_output():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_response(
        "I developed a Python project... "
        "I I was initially nervous, but I successfully "
        "completed the work."
    )

    assert "raw_text" in result
    assert "behavioral_confidence_score" in result
    assert "behavioral_confidence_level" in result
    assert "stress_level" in result
    assert "signals" in result

    assert "confidence" in result["signals"]
    assert "long_pauses" in result["signals"]
    assert "repeated_words" in result["signals"]
    assert "stress" in result["signals"]


def test_stress_signal_in_complete_analysis():
    analyzer = ConfidenceStressAnalyzer()

    result = analyzer.analyze_response(
        "I felt nervous and stressed while presenting."
    )

    assert (
        result["signals"]["stress"]["stress_count"]
        >= 2
    )
