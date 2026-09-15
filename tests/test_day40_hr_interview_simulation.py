from scoring.hr_interview_simulation import (
    HRInterviewSimulationEngine,
)


def test_simulation_engine_initialization():
    engine = HRInterviewSimulationEngine()

    assert engine.interview_engine is not None
    assert engine.aptitude_engine is not None
    assert engine.summary_generator is not None


def test_candidate_profiles_are_defined():
    engine = HRInterviewSimulationEngine()

    assert len(engine.CANDIDATES) == 4

    candidate_types = {
        candidate["candidate_type"]
        for candidate in engine.CANDIDATES
    }

    assert candidate_types == {
        "confident",
        "hesitant",
        "inexperienced",
        "overqualified",
    }


def test_single_session_simulation():
    engine = HRInterviewSimulationEngine()

    result = engine.simulate_session(
        engine.CANDIDATES[0]
    )

    assert result["candidate_name"] == (
        "Ananya Menon"
    )

    assert result["candidate_type"] == (
        "confident"
    )

    assert "interview_state" in result
    assert "follow_up_events" in result
    assert "interview_evaluation" in result
    assert "aptitude_evaluation" in result
    assert "summary" in result


def test_follow_up_events_are_generated():
    engine = HRInterviewSimulationEngine()

    result = engine.simulate_session(
        engine.CANDIDATES[0]
    )

    assert len(
        result["follow_up_events"]
    ) == 3

    for event in result["follow_up_events"]:
        assert "follow_up_eligible" in event
        assert "analysis" in event


def test_interview_evaluation_is_present():
    engine = HRInterviewSimulationEngine()

    result = engine.simulate_session(
        engine.CANDIDATES[0]
    )

    evaluation = result[
        "interview_evaluation"
    ]

    assert "interview_score" in evaluation
    assert "interview_level" in evaluation
    assert "score_breakdown" in evaluation

    assert 0 <= evaluation[
        "interview_score"
    ] <= 100


def test_aptitude_evaluation_is_present():
    engine = HRInterviewSimulationEngine()

    result = engine.simulate_session(
        engine.CANDIDATES[0]
    )

    evaluation = result[
        "aptitude_evaluation"
    ]

    assert "aptitude_score" in evaluation
    assert "aptitude_level" in evaluation
    assert "score_breakdown" in evaluation

    assert 0 <= evaluation[
        "aptitude_score"
    ] <= 100


def test_summary_is_generated():
    engine = HRInterviewSimulationEngine()

    result = engine.simulate_session(
        engine.CANDIDATES[0]
    )

    summary = result["summary"]

    assert summary["report_type"] == (
        "AI Interview Summary Report"
    )

    assert "candidate" in summary
    assert "summary" in summary
    assert "evaluation" in summary
    assert "insights" in summary
    assert "recommendation" in summary


def test_manual_comparison():
    engine = HRInterviewSimulationEngine()

    simulation = {
        "interview_evaluation": {
            "interview_score": 80.0,
        },
        "aptitude_evaluation": {
            "aptitude_score": 75.0,
        },
    }

    manual = {
        "interview_score": 85.0,
        "aptitude_score": 70.0,
        "performance_level": "excellent",
    }

    result = engine.compare_with_manual_evaluation(
        simulation,
        manual,
    )

    assert result[
        "interview_absolute_error"
    ] == 5.0

    assert result[
        "aptitude_absolute_error"
    ] == 5.0

    assert result[
        "classification_agreement"
    ] is True


def test_inconsistency_detection():
    engine = HRInterviewSimulationEngine()

    comparison = {
        "interview_absolute_error": 20.0,
        "aptitude_absolute_error": 18.0,
        "classification_agreement": False,
    }

    result = engine.identify_scoring_inconsistencies(
        comparison
    )

    assert len(result) == 3


def test_improvement_recommendations():
    engine = HRInterviewSimulationEngine()

    results = [
        {
            "comparison": {
                "classification_agreement": False,
                "interview_absolute_error": 20.0,
                "aptitude_absolute_error": 18.0,
            }
        }
    ]

    recommendations = (
        engine.generate_improvement_recommendations(
            results
        )
    )

    assert len(recommendations) >= 3


def test_all_candidate_simulations():
    engine = HRInterviewSimulationEngine()

    report = engine.run_all_simulations()

    assert report["report_type"] == (
        "HR Interview End-to-End Simulation Report"
    )

    assert report["simulation_count"] == 4

    assert len(report["results"]) == 4

    assert (
        report["accuracy_evaluation"][
            "total_classifications"
        ]
        == 4
    )


def test_all_candidate_types_are_reported():
    engine = HRInterviewSimulationEngine()

    report = engine.run_all_simulations()

    types = {
        result["candidate"]["type"]
        for result in report["results"]
    }

    assert types == {
        "confident",
        "hesitant",
        "inexperienced",
        "overqualified",
    }


def test_accuracy_evaluation_structure():
    engine = HRInterviewSimulationEngine()

    report = engine.run_all_simulations()

    accuracy = report[
        "accuracy_evaluation"
    ]

    assert "classification_accuracy" in accuracy
    assert "classification_matches" in accuracy
    assert "total_classifications" in accuracy
    assert "interview_mean_absolute_error" in accuracy
    assert "aptitude_mean_absolute_error" in accuracy

    assert 0 <= accuracy[
        "classification_accuracy"
    ] <= 100


def test_improvement_recommendations_in_report():
    engine = HRInterviewSimulationEngine()

    report = engine.run_all_simulations()

    recommendations = report[
        "improvement_recommendations"
    ]

    assert isinstance(
        recommendations,
        list,
    )

    assert len(recommendations) >= 2


def test_text_report_generation():
    engine = HRInterviewSimulationEngine()

    report = engine.run_all_simulations()

    text = engine.generate_text_report(
        report
    )

    assert (
        "HR INTERVIEW END-TO-END SIMULATION REPORT"
        in text
    )

    assert "CANDIDATE SIMULATIONS" in text
    assert "ACCURACY EVALUATION" in text
    assert "IMPROVEMENT RECOMMENDATIONS" in text

    assert "Ananya Menon" in text
    assert "Rahul Nair" in text
    assert "Arjun Kumar" in text
    assert "Meera Thomas" in text


def test_score_classification_boundaries():
    engine = HRInterviewSimulationEngine()

    assert (
        engine._classify_score(90)
        == "excellent"
    )

    assert (
        engine._classify_score(70)
        == "good"
    )

    assert (
        engine._classify_score(55)
        == "moderate"
    )

    assert (
        engine._classify_score(30)
        == "needs_improvement"
    )
