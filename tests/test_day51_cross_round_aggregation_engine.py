import pytest
from scoring.cross_round_aggregation_engine import CrossRoundAggregationEngine
def test_weighted_aggregation():
    r=CrossRoundAggregationEngine().aggregate("Data Scientist",{"ats":80,"technical_interview":90})
    assert r["hiring_fit_score"]==pytest.approx(86.0) and len(r["missing_rounds"])==3
def test_renormalizes_available_rounds():
    assert CrossRoundAggregationEngine().aggregate("Business Analyst",{"ats":80,"screening":60})["hiring_fit_score"]==pytest.approx(72.5)
def test_empty_scores():
    assert CrossRoundAggregationEngine().aggregate("Data Scientist",{})["hiring_fit_score"] is None
@pytest.mark.parametrize("v",[-1,101,True,"80"])
def test_invalid_score(v):
    with pytest.raises(ValueError): CrossRoundAggregationEngine().aggregate("Data Scientist",{"ats":v})
def test_unknown_role():
    with pytest.raises(ValueError): CrossRoundAggregationEngine().aggregate("Unknown",{})
def test_custom_weights_validation():
    with pytest.raises(ValueError): CrossRoundAggregationEngine({"x":{"ats":1}})
def test_candidate_id():
    assert CrossRoundAggregationEngine().aggregate("Data Scientist",{"ats":50},"C1")["candidate_id"]=="C1"
