"""Run the synthetic Zecpath end-to-end demo from the repository root."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.hiring_pipeline_simulator import HiringPipelineSimulator
from utils.recruiter_report_formatter import RecruiterReportFormatter

DATA = ROOT / "data" / "demo" / "day63_hiring_pipeline_demo.json"


def main():
    dataset = json.loads(DATA.read_text(encoding="utf-8"))
    simulator = HiringPipelineSimulator()
    formatter = RecruiterReportFormatter()
    print(f"Dataset: {dataset['dataset_name']} (synthetic={dataset['synthetic_data']})")
    for item in dataset["candidates"]:
        payload = {
            "candidate": {"candidate_id": item["candidate_id"], "role": item["role"]},
            **{key: item[key] for key in (
                "resume_text", "ats_inputs", "screening_responses", "hr_answers",
                "technical_responses", "machine_submissions"
            )}
        }
        result = simulator.run(payload)
        report = formatter.format(result)
        print("-" * 72)
        print(f"{item['candidate_id']} | {item['name']} | {item['role']}")
        print("Round scores:", json.dumps(report["round_scores"], sort_keys=True))
        print(f"Fit: {report['hiring_fit_score']:.2f}/100 | Coverage: {report['coverage_percent']:.1f}%")
        print("Recommendation:", report["recommendation"])
        print("Human review required:", report["human_review_required"])


if __name__ == "__main__":
    main()
