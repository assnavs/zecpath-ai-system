# Zecpath AI System — Internship Portfolio

## Project
**Zecpath AI System** — modular recruitment workflow and decision-support prototype.

## Internship context
Prepared as a project portfolio for the Data Science Engineer Internship at Zecser Business LLP. This portfolio describes the supplied repository snapshot and implemented modules; it does not claim confidential company internals or production deployment.

## Problem explored
Recruitment evidence can be distributed across resume review, screening and interview stages. The project explores a modular workflow that organizes structured evaluation signals and presents a consolidated recruiter-facing summary.

## System components
- `parsers/` — resume and job-description parsing, normalization and extraction.
- `scoring/` — ATS, screening, HR interview, technical evaluation, aggregation and scoring utilities.
- `screening_ai/` — screening conversation, intent, shortlisting and report components.
- `interview_ai/` — interview flows, technical interview, machine test and recommendation components.
- `ats_engine/` — FastAPI interface and ATS API implementation.
- `utils/` — pipeline simulation, validation, security/governance, observability and report formatting.
- `data/` — configurations, test inputs and synthetic demo records.
- `tests/` — regression and module tests.
- `docs/` — day-wise technical documentation and reports.

## Demonstration
The synthetic demo runs the five score rounds, role-weighted aggregation and recommendation generation. It does not exercise actual file upload-to-parser integration or production services.

## Responsible-use boundary
Scores are heuristic/rubric-based decision-support signals. They are not objective measures of human worth, and they must not replace human review. No production accuracy, fairness, time-saving or hiring-outcome improvement has been established.

## Key learning outcomes
- Modular Python project organization and test-driven iteration.
- Resume data parsing and structured feature handling.
- Scoring and aggregation with explicit weights and coverage.
- API contracts, validation and error handling.
- Testing, documentation, version control and technical handover.
- Responsible AI limitations, privacy and human oversight.
