import pytest
from interview_ai.machine_test_engine import MachineTestEngine

def task(kind="coding"):
    return {"task_id": "T1", "task_type": kind, "time_limit_seconds": 600}

def sub(**kwargs):
    d = {"time_used_seconds": 300, "tests_passed": 8, "tests_total": 10, "code_quality_score": 80, "problem_solving_approach_score": 70}
    d.update(kwargs)
    return d

@pytest.mark.parametrize("kind", ["coding", "debugging", "file_based", "mini_system_design"])
def test_task_types(kind):
    assert 0 <= MachineTestEngine().evaluate_submission(task(kind), sub())["final_score"] <= 100

def test_correctness_from_tests():
    assert MachineTestEngine().evaluate_submission(task(), sub(tests_passed=5))["dimension_scores"]["correctness"] == 50

def test_time_limit_penalty():
    r = MachineTestEngine().evaluate_submission(task(), sub(time_used_seconds=1200))
    assert r["dimension_scores"]["efficiency"] == 0 and not r["within_time_limit"]

def test_code_is_not_executed():
    r = MachineTestEngine().evaluate_submission(task(), sub(code_snapshots=[{"version": 1}], execution_results=[{"status": "passed"}]))
    assert not r["execution_performed_by_engine"] and len(r["code_snapshots"]) == 1

def test_invalid_test_counts():
    with pytest.raises(ValueError): MachineTestEngine().evaluate_submission(task(), sub(tests_passed=11))

def test_session_aggregation():
    assert MachineTestEngine().evaluate_session([{"task": task(), "submission": sub()}])["task_count"] == 1
