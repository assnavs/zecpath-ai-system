import json
from pathlib import Path

from utils.hiring_pipeline_simulator import HiringPipelineSimulator
from utils.recruiter_report_formatter import RecruiterReportFormatter


def test_all_synthetic_demo_candidates_complete_pipeline_and_report():
    root = Path(__file__).resolve().parents[1]
    dataset = json.loads((root / "data/demo/day63_hiring_pipeline_demo.json").read_text(encoding="utf-8"))
    simulator = HiringPipelineSimulator()
    formatter = RecruiterReportFormatter()

    assert dataset["synthetic_data"] is True
    assert len(dataset["candidates"]) >= 1

    for item in dataset["candidates"]:
        payload = {
            "candidate": {"candidate_id": item["candidate_id"], "role": item["role"]},
            **{key: item[key] for key in (
                "resume_text", "ats_inputs", "screening_responses", "hr_answers",
                "technical_responses", "machine_submissions"
            )}
        }
        result = simulator.run(payload)
        assert [stage["stage"] for stage in result["stages"]][-1] == "final_decision"
        assert set(result["round_scores"]) == set(formatter.REQUIRED_ROUNDS)
        assert 0 <= result["aggregation"]["hiring_fit_score"] <= 100
        assert result["human_review_required"] is True
        report = formatter.format(result)
        assert report["human_review_required"] is True
        assert report["candidate"]["candidate_id"] == item["candidate_id"]
