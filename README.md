# Zecpath AI System

A modular Python recruitment workflow and decision-support prototype developed during the Data Science Engineer Internship at **Zecser Business LLP**.

> **Important scope note:** This repository is an internship prototype. It is not a validated autonomous hiring system. Scores and recommendations are advisory signals; an authorized human reviewer must make every hiring decision.

## Workflow

Resume parsing and normalization → ATS scoring → screening → HR interview → technical interview → machine-test evaluation → cross-round aggregation → recommendation → recruiter report → human review.

## Repository layout

```text
ats_engine/       FastAPI endpoints and ATS API
parsers/          Resume and job-description parsing/normalization
screening_ai/     Screening flow, intent, shortlisting and reports
interview_ai/     Interview, technical task and recommendation modules
scoring/          Scoring, aggregation and evaluation engines
utils/            Simulation, validation, observability and report utilities
data/             Configuration, examples and synthetic demo inputs
tests/            Automated tests
docs/             Day-wise technical documentation and handover material
scripts/          Repeatable demonstration scripts
```

## Requirements and setup (Windows PowerShell)

Use Python 3.11 as the tested project environment.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

## Run the synthetic final demo

From the repository root:

```powershell
python scripts/run_final_demo.py
```

The demo uses synthetic candidate records from `data/demo/day63_hiring_pipeline_demo.json`. It passes structured inputs to the deterministic simulator. It does not demonstrate a production upload-to-parser integration, production model serving, or execution of candidate-submitted code.

## Key implementation notes

- Aggregation uses role-specific configured weights and renormalizes over available rounds.
- Coverage is reported separately so missing stages remain visible.
- Recommendation thresholds are configurable in the recommendation engine.
- Recommendation confidence is a coverage-based heuristic, not a statistical probability.
- The machine-test component evaluates supplied test outcomes and rubric values; it does not execute untrusted code.
- API resume/job stores are in-memory demonstration stores, not durable production storage.
- Observability and audit utilities are in-process foundations.

## Testing

```powershell
python -m pytest -v
```

The full suite requires all packages in `requirements.txt`, including `sentence-transformers`. Review warnings and environment-specific collection errors rather than treating an incomplete run as a full pass.

## Documentation

- `docs/day66/` — demo script and architecture diagrams
- `docs/day67/` — mock demo feedback and stakeholder Q&A
- `docs/day68/` — final validation and bug-fix report
- `docs/day69/` — AI roadmap and internship portfolio
- `docs/day70/` — final demo and handover guide
- Earlier day-wise documentation remains under `docs/day*/`.

## Responsible use

Do not use real applicant data in public demonstrations. Before any real-world pilot, complete privacy, security, fairness, accessibility, legal, model evaluation and operational reviews. Keep a human reviewer accountable for final decisions.
