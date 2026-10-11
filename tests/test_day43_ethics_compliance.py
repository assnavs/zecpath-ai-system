import json
from pathlib import Path

from parsers.resume_normalizer import ResumeNormalizer
from scoring.fair_scoring_engine import FairScoringEngine
from scoring.unified_scoring_engine import UnifiedScoringEngine


ROOT = Path(__file__).resolve().parents[1]


def test_day43_demographic_attributes_are_configured_for_masking():
    config = json.loads(
        (ROOT / "data" / "fairness_configuration.json").read_text(
            encoding="utf-8"
        )
    )
    configured = set(config["personal_attributes_to_mask"])
    expected = {
        "name", "email", "phone", "address", "date_of_birth", "dob",
        "gender", "marital_status", "nationality", "religion",
        "race", "ethnicity", "age", "disability", "sexual_orientation",
        "gender_identity", "pronouns", "place_of_birth", "postal_code",
    }
    assert expected.issubset(configured)


def test_day43_configured_attributes_are_masked_case_insensitively():
    normalizer = ResumeNormalizer(
        json.loads(
            (ROOT / "data" / "fairness_configuration.json").read_text(
                encoding="utf-8"
            )
        )["personal_attributes_to_mask"]
    )
    resume = {
        "Race": "Example",
        " ETHNICITY ": "Example",
        "age": 28,
        "Gender_Identity": "Example",
        "postal_code": "00000",
        "skills": ["Python", "SQL"],
    }
    normalized = normalizer.normalize_resume(resume)
    assert normalized["race"] == "[MASKED]"
    assert normalized["ethnicity"] == "[MASKED]"
    assert normalized["age"] == "[MASKED]"
    assert normalized["gender_identity"] == "[MASKED]"
    assert normalized["postal_code"] == "[MASKED]"
    assert normalized["skills"] == ["python", "sql"]


def test_day43_keyword_cap_and_scoring_settings_remain_unchanged():
    engine = FairScoringEngine()
    assert engine.keyword_score_cap == 85
    assert engine.minimum_score == 0
    assert engine.maximum_score == 100


def test_day43_fairness_review_flags_high_keyword_dependency():
    engine = FairScoringEngine()
    result = engine.evaluate_bias_indicators(
        {
            "keyword_match": 0.75,
            "semantic_similarity": 0.20,
        },
        personal_attributes_masked=True,
    )
    assert result["requires_review"] is True
    assert "High keyword dependency detected." in result["bias_flags"]


def test_day43_unified_score_is_not_described_as_automatic_hiring():
    engine = UnifiedScoringEngine()
    role = next(iter(engine.config["role_weights"]))
    result = engine.calculate_unified_score(
        candidate_id="test-candidate",
        job_role=role,
        ats_score=75,
    )
    assert "not an automatic hiring decision" in result["decision_note"]


def test_day43_required_documents_exist():
    docs = ROOT / "docs" / "day43"
    required = {
        "ai_ethics_documentation.md",
        "fairness_review_notes.md",
        "compliance_readiness_report.md",
    }
    assert required.issubset({path.name for path in docs.iterdir()})
