import pytest
from interview_ai.integrity_detection_engine import IntegrityDetectionEngine

def test_consent_required():
    assert not IntegrityDetectionEngine().evaluate_events([{"type": "tab_switch"}])["analysis_performed"]

def test_tab_switch_threshold():
    r = IntegrityDetectionEngine().evaluate_events([{"type": "tab_switch"} for _ in range(3)], True)
    assert r["risk_tag"] == "review_required" and r["malpractice_conclusion"] is None

def test_looking_away_not_a_malpractice_flag():
    r = IntegrityDetectionEngine().evaluate_events([{"type": "looking_away_indicator"} for _ in range(5)], True)
    assert r["risk_tag"] == "no_threshold_flag" and r["alerts"][0]["tag"] == "not_scored"

def test_external_voice_threshold():
    r = IntegrityDetectionEngine().evaluate_events([{"type": "external_voice_indicator"} for _ in range(2)], True)
    assert r["risk_tag"] == "review_required"

def test_unknown_event():
    with pytest.raises(ValueError): IntegrityDetectionEngine().evaluate_events([{"type": "unknown"}], True)
