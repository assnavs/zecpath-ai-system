# Day 70 — Final Demo and Knowledge Transfer Guide

## Demonstration sequence
1. Introduce the problem and the system's decision-support scope.
2. Explain the module architecture and hiring pipeline diagram.
3. Run `python scripts/run_final_demo.py` from the repository root.
4. Explain round scores, weighted aggregation, coverage and recommendation.
5. Show recruiter report formatting and observability foundations.
6. Review tests, documentation, limitations and future roadmap.
7. Invite evaluation questions and confirm handover contents.

## Code walkthrough order
1. `parsers/` — parsing and normalization boundaries.
2. `scoring/ats_scoring_engine.py` — ATS scoring.
3. `scoring/screening_scoring_engine.py` and `scoring/hr_interview_scoring_engine.py` — screening and HR evaluation.
4. `scoring/technical_skill_scoring_engine.py` and `interview_ai/machine_test_engine.py` — technical and machine-test evaluation.
5. `scoring/cross_round_aggregation_engine.py` — weighted aggregation and coverage.
6. `interview_ai/final_recommendation_engine.py` — advisory recommendation.
7. `utils/hiring_pipeline_simulator.py` — deterministic integration simulation.
8. `utils/recruiter_report_formatter.py` — presentation-only report.
9. `ats_engine/api.py` — API routes and current in-memory boundaries.

## Setup (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
python scripts/run_final_demo.py
```
If PowerShell blocks activation, use the environment activation policy approved for the machine or invoke `venv\Scripts\python.exe` directly.

## Handover inventory
- Source code and configuration in the repository.
- Day-wise documentation and reports in `docs/`.
- Synthetic demo data in `data/demo/`.
- Automated tests in `tests/`.
- Final demo slides and speaker script.
- Architecture diagrams in Mermaid format.
- AI roadmap and portfolio summary.

## Known boundaries to disclose
- In-memory API stores are not durable.
- Demo simulator consumes structured inputs; it does not prove production end-to-end ingestion.
- Machine-test module does not execute untrusted submitted code.
- Some scores are heuristic/rubric-based.
- Recommendation confidence is a heuristic, not a probability.
- Observability and audit helpers are in-process foundations.
- Human review remains required for all hiring decisions.
