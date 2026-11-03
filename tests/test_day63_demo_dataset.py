import json
from pathlib import Path

def test_demo_dataset_has_required_pipeline_inputs():
    path=Path("data/demo/day63_hiring_pipeline_demo.json")
    data=json.loads(path.read_text(encoding="utf-8"))
    assert data["synthetic_data"] is True
    assert len(data["job_descriptions"]) >= 1
    assert len(data["candidates"]) >= 3
    required={"candidate_id","role","resume_text","ats_inputs","screening_responses",
              "hr_answers","technical_responses","machine_submissions"}
    for candidate in data["candidates"]:
        assert candidate["candidate_id"] and candidate["role"]
        assert candidate["resume_text"].strip()
        assert {"ats_inputs","screening_responses","hr_answers","technical_responses","machine_submissions"} <= set(candidate)
