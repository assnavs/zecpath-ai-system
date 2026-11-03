# Day 63 — Demo Dataset Creation

## Dataset
`data/demo/day63_hiring_pipeline_demo.json` contains:
- two fictional job descriptions (Data Scientist and Business Analyst)
- three synthetic candidate profiles with varied evidence quality
- resume text, ATS component inputs, screening rubric responses, HR answers, technical responses and machine-test submissions
- interpretation and privacy guidance

## Usage
Load the JSON with Python and select one candidate's structured inputs to feed the existing `HiringPipelineSimulator`. The sample includes all stage inputs required by the simulator. The simulator's `resume_text` field is supplied structured text; it does not exercise PDF/DOCX upload or OCR.

```python
import json
from utils.hiring_pipeline_simulator import HiringPipelineSimulator

with open("data/demo/day63_hiring_pipeline_demo.json", encoding="utf-8") as f:
    demo = json.load(f)

# Candidate payloads can be assembled from candidate fields:
candidate = demo["candidates"][0]
payload = {
    "candidate": {"candidate_id": candidate["candidate_id"], "role": candidate["role"]},
    "resume_text": candidate["resume_text"],
    "ats_inputs": candidate["ats_inputs"],
    "screening_responses": candidate["screening_responses"],
    "hr_answers": candidate["hr_answers"],
    "technical_responses": candidate["technical_responses"],
    "machine_submissions": candidate["machine_submissions"],
}
result = HiringPipelineSimulator().run(payload)
```

All records are invented for software demonstration. `profile_quality` is a narrative descriptor, not a ground-truth label. Do not use these records to tune or claim model accuracy.
