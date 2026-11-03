import pytest
from scoring.optimization_refinement_engine import OptimizationRefinementEngine
def test_confusion_metrics():
    r=OptimizationRefinementEngine.confusion_metrics([1,1,0,0],[1,0,1,0])
    assert (r["true_positive"],r["false_positive"],r["false_negative"],r["true_negative"])==(1,1,1,1)
    assert r["f1_score"]==.5
def test_threshold_metrics():
    r=OptimizationRefinementEngine().evaluate_threshold([{"score":90,"actual_positive":1},{"score":20,"actual_positive":0}],70)
    assert r["metrics"]["accuracy"]==1 and not r["production_threshold_changed"]
def test_empty_validation():
    with pytest.raises(ValueError): OptimizationRefinementEngine().evaluate_threshold([],50)
def test_bad_labels():
    with pytest.raises(ValueError): OptimizationRefinementEngine.confusion_metrics([2],[1])
def test_consistency():
    assert OptimizationRefinementEngine.score_consistency({"ats":70,"technical":90})["range"]==20
def test_empty_consistency():
    assert OptimizationRefinementEngine.score_consistency({})["mean"] is None
