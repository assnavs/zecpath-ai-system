from interview_ai.hiring_intelligence_report_generator import HiringIntelligenceReportGenerator
def test_report_sections_and_insights():
    r=HiringIntelligenceReportGenerator().generate({"candidate_id":"C1"},{"hiring_fit_score":82},{"recommendation":"Selected"},
    {"ats":{"score":90},"technical_interview":{"score":40},"integrity":{"risk_flags":["review"]}})
    assert len(r["strengths"])==1 and len(r["weaknesses"])==1 and "review" in r["risk_indicators"]
def test_missing_sections_are_none():
    r=HiringIntelligenceReportGenerator().generate({}, {}, {})
    assert r["ats_summary"] is None and r["machine_test_performance"] is None
def test_report_limitations():
    assert len(HiringIntelligenceReportGenerator().generate({}, {}, {})["limitations"])==3
