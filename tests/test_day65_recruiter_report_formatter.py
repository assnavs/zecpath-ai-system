import pytest
from utils.recruiter_report_formatter import RecruiterReportFormatter

def sample():
    return {
        "candidate":{"candidate_id":"DEMO-1","role":"Data Scientist"},
        "round_scores":{"ats":80,"screening":75,"hr_interview":78,"technical_interview":82,"machine_test":79},
        "aggregation":{"hiring_fit_score":79.5,"coverage_percent":100},
        "recommendation":{"recommendation":"Hold / Review","explanation":["Human review required."]}
    }

def test_report_contains_required_sections():
    report=RecruiterReportFormatter().format(sample())
    assert report["candidate"]["candidate_id"]=="DEMO-1"
    assert report["hiring_fit_score"]==79.5
    assert report["human_review_required"] is True
    assert "resume_text" not in report

def test_missing_round_is_rejected():
    data=sample(); del data["round_scores"]["ats"]
    with pytest.raises(ValueError,match="Missing round scores"):
        RecruiterReportFormatter().format(data)

def test_invalid_score_is_rejected():
    data=sample(); data["round_scores"]["ats"]=float("nan")
    with pytest.raises(ValueError):
        RecruiterReportFormatter().format(data)

def test_missing_recommendation_is_rejected():
    data=sample(); data["recommendation"]={}
    with pytest.raises(ValueError):
        RecruiterReportFormatter().format(data)
