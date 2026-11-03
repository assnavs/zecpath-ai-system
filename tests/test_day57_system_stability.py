import pytest
from utils.system_stability_validator import SystemStabilityValidator as V

@pytest.mark.parametrize("score",[0,50,100])
def test_valid_scores(score): assert V.validate_score(score)==float(score)

@pytest.mark.parametrize("score",[True,-1,101,float("nan"),float("inf"),"80",None])
def test_invalid_scores(score):
    with pytest.raises(ValueError): V.validate_score(score,"ats_score")

def test_success_envelope():
    assert V.validate_success_envelope({"success":True,"data":{"id":"A"}})=={"id":"A"}

@pytest.mark.parametrize("payload",[None,{},{"success":False,"data":{}},{"success":True}])
def test_invalid_success_envelope(payload):
    with pytest.raises(ValueError): V.validate_success_envelope(payload)

def test_error_contract():
    assert V.normalize_error("bad input","VALIDATION_ERROR")=={
      "success":False,"error":{"code":"VALIDATION_ERROR","message":"bad input"}}
