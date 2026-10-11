import json

import pytest

from scoring.unified_scoring_engine import UnifiedScoringEngine


@pytest.fixture
def engine():
    return UnifiedScoringEngine()


def test_configuration_exists(engine):
    assert engine.CONFIG_PATH.exists()


def test_all_rounds_produce_weighted_score(engine):
    result = engine.calculate_unified_score(
        candidate_id="C001",
        job_role="Data Analyst",
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
    )

    # 80 * .35 + 60 * .25 + 90 * .40 = 79
    assert result["unified_score"] == 79.0
    assert result["hiring_fit_percentage"] == 79.0
    assert result["classification"] == "good"


def test_role_specific_weights_are_applied(engine):
    result = engine.calculate_unified_score(
        candidate_id="C002",
        job_role="Business Analyst",
        ats_score=80,
        screening_score=60,
        hr_interview_score=90,
    )

    # 80 * .30 + 60 * .30 + 90 * .40 = 78
    assert result["unified_score"] == 78.0
    assert result["configured_role_weights"]["screening"] == 0.30


def test_missing_round_is_recorded_and_weights_renormalized(engine):
    result = engine.calculate_unified_score(
        candidate_id="C003",
        job_role="Data Analyst",
        ats_score=80,
        screening_score=None,
        hr_interview_score=100,
    )

    assert result["missing_rounds"] == ["screening"]
    assert result["unified_score"] == 90.67
    assert "screening" not in result["applied_weights"]


def test_at_least_one_score_is_required(engine):
    with pytest.raises(ValueError, match="At least one"):
        engine.calculate_unified_score(
            candidate_id="C004",
            job_role="Data Analyst",
        )


@pytest.mark.parametrize(
    "score",
    [-1, 101, float("nan"), float("inf"), True, "80"],
)
def test_invalid_scores_are_rejected(engine, score):
    with pytest.raises(ValueError):
        engine.calculate_unified_score(
            candidate_id="C005",
            job_role="Data Analyst",
            ats_score=score,
        )


@pytest.mark.parametrize("score", [0, 100])
def test_score_boundaries(engine, score):
    result = engine.calculate_unified_score(
        candidate_id="C006",
        job_role="Data Analyst",
        ats_score=score,
        screening_score=score,
        hr_interview_score=score,
    )

    assert result["unified_score"] == score
    assert result["hiring_fit_percentage"] == score


def test_unsupported_role_is_rejected(engine):
    with pytest.raises(ValueError, match="Unsupported job role"):
        engine.calculate_unified_score(
            candidate_id="C007",
            job_role="Unknown Role",
            ats_score=80,
        )


@pytest.mark.parametrize(
    "weights",
    [
        {"ats": 0.5, "screening": 0.2, "hr_interview": 0.2},
        {"ats": -0.1, "screening": 0.5, "hr_interview": 0.6},
        {"ats": 1, "screening": 0, "hr_interview": 0},
    ],
)
def test_invalid_weight_configuration_is_rejected(tmp_path, weights):
    config = {
        "score_range": {"minimum": 0, "maximum": 100},
        "missing_score_policy": "renormalize_available_weights",
        "default_weights": {
            "ats": 0.35, "screening": 0.25, "hr_interview": 0.40
        },
        "role_weights": {"Data Analyst": weights},
        "thresholds": {"excellent": 80, "good": 65, "moderate": 50},
    }

    path = tmp_path / "invalid_config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(ValueError, match="Weights must"):
        UnifiedScoringEngine(str(path))


def test_unified_result_contains_required_fields(engine):
    result = engine.calculate_unified_score(
        candidate_id="C008",
        job_role="Data Scientist",
        ats_score=90,
        screening_score=85,
        hr_interview_score=88,
    )

    required = {
        "candidate_id",
        "job_role",
        "round_scores",
        "configured_role_weights",
        "applied_weights",
        "unified_score",
        "hiring_fit_percentage",
        "classification",
        "missing_rounds",
        "decision_note",
    }

    assert required.issubset(result)
    assert sum(result["configured_role_weights"].values()) == pytest.approx(1)
    assert sum(result["applied_weights"].values()) == pytest.approx(1)


def test_empty_candidate_id_is_rejected(engine):
    with pytest.raises(ValueError, match="candidate_id"):
        engine.calculate_unified_score(
            candidate_id=" ",
            job_role="Data Analyst",
            ats_score=80,
        )


def test_empty_role_is_rejected(engine):
    with pytest.raises(ValueError, match="job_role"):
        engine.calculate_unified_score(
            candidate_id="C009",
            job_role=" ",
            ats_score=80,
        )
