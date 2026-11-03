import pytest
from interview_ai.final_recommendation_engine import FinalRecommendationEngine
def ag(s=85,c=100): return {"hiring_fit_score":s,"coverage_percent":c}
def test_selected(): assert FinalRecommendationEngine().recommend(ag())["recommendation"]=="Selected"
def test_low_coverage_holds(): assert FinalRecommendationEngine().recommend(ag(90,20))["recommendation"]=="Hold / Review"
def test_high_risk_holds():
    r=FinalRecommendationEngine().recommend(ag(),[{"severity":"high"}])
    assert r["recommendation"]=="Hold / Review" and not r["automated_hiring_decision"]
def test_low_score_rejected(): assert FinalRecommendationEngine().recommend(ag(40))["recommendation"]=="Rejected"
def test_missing_score_holds(): assert FinalRecommendationEngine().recommend(ag(None))["recommendation"]=="Hold / Review"
def test_invalid_thresholds():
    with pytest.raises(ValueError): FinalRecommendationEngine(50,60)
def test_invalid_risk():
    with pytest.raises(ValueError): FinalRecommendationEngine().recommend(ag(),[{"severity":"critical"}])
