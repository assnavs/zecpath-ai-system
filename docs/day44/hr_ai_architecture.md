# Day 44 — HR Interview AI Architecture

## 1. Objective

Document the existing HR Interview AI components, their responsibilities, data flow, scoring configuration, and integration boundaries in the Zecpath AI System.

## 2. Architecture Overview

The interview workflow is implemented through Python modules. The ATS REST API is a separate FastAPI application in `ats_engine/api.py`.

```text
Candidate Profile / Role
        |
        v
InterviewAI
(interview_ai/interview.py)
        |
        +--> HR screening dataset
        |
        +--> Interview questions and phases
        |
        v
Candidate Responses
        |
        v
DynamicFollowUpEngine
(interview_ai/follow_up_engine.py)
        |
        v
HRInterviewScoringEngine
(scoring/hr_interview_scoring_engine.py)
        |
        +--> CommunicationScoringEngine
        |
        +--> ConfidenceSentimentEngine
        |
        v
Interview Evaluation
        |
        v
Interview Summary Generator
(scoring/interview_summary_generator.py)
        |
        v
Structured Recruiter Report
```

The diagram describes the documented component flow. Exact runtime orchestration should be verified against the relevant implementation before introducing a new integration.

## 3. Component Responsibilities

### InterviewAI

Location: `interview_ai/interview.py`

Responsibilities include:
- Initializing an interview for a supported role.
- Validating experience level (`fresher` or `experienced`).
- Loading role-based questions from `data/hr_screening_dataset.json`.
- Classifying configured roles as technical or non-technical.
- Managing interview phases and state.
- Capturing responses and tracking follow-up eligibility.

The documented phases are `introduction`, `core_hr_questions`, `role_based_evaluation`, and `closing`.

### DynamicFollowUpEngine

Location: `interview_ai/follow_up_engine.py`

Responsibilities include:
- Detecting empty, vague, very short, short, and detailed responses.
- Selecting clarification, deepening, example, or scenario follow-up behavior.
- Tracking follow-up state.
- Limiting follow-ups to two.
- Suppressing repeated follow-up prompts.

Follow-up decisions use configured text and response-length signals. They should not be interpreted as validated measures of a candidate's personality or ability.

### HRInterviewScoringEngine

Location: `scoring/hr_interview_scoring_engine.py`

The engine combines:
- Answer relevance.
- Communication quality.
- Confidence indicators.
- Answer consistency.

Configuration: `data/hr_interview_scoring_configuration.json`.

| Dimension | Weight |
|---|---:|
| Answer relevance | 35% |
| Communication | 25% |
| Confidence | 25% |
| Consistency | 15% |

Scores are normalized to the 0?100 range. The first answer receives a consistency score of 100 when no previous answer is available; this is a default, not evidence of demonstrated consistency.

### Supporting Scoring Components

- `scoring/communication_scoring_engine.py`: communication-related evaluation.
- `scoring/confidence_sentiment_engine.py`: confidence and sentiment signals.
- `scoring/aptitude_logic_engine.py`: aptitude and logic evaluation in the broader workflow.
- `scoring/interview_summary_generator.py`: creates structured and recruiter-oriented summaries from evaluation inputs.

### ATS REST API

Location: `ats_engine/api.py`

The FastAPI application exposes resume upload, resume parsing, ATS scoring, shortlisting, job-status, and health endpoints. Its documented purpose is ATS processing; the existence of these routes does not establish dedicated HTTP endpoints for every HR interview operation.

## 4. Data Flow

1. Select a supported role and experience level.
2. Load role-specific questions from the HR screening dataset.
3. Manage question phases and capture candidate answers.
4. Analyze responses for follow-up eligibility.
5. Evaluate answer relevance, communication, confidence, and consistency.
6. Pass evaluation outputs to summary/reporting components where integrated.
7. Present results for recruiter review.

## 5. Configuration and Data Files

| File | Purpose |
|---|---|
| `data/hr_screening_dataset.json` | Role-based interview questions |
| `data/hr_interview_scoring_configuration.json` | Score weights, thresholds, and range |
| `data/interview_summary_configuration.json` | Summary generation configuration |
| `data/interview_summary_template.json` | Summary report structure |
| `data/sample_hr_interview_summary_reports.json` | Sample generated summaries |

## 6. API Boundary

The current REST API is implemented in `ats_engine/api.py`. The interview and scoring modules listed above are Python components. Do not describe a method as an HTTP endpoint unless a corresponding route is implemented and tested.

A future interview API could wrap interview initialization, question retrieval, response submission, and report retrieval, but such endpoints are proposals and are not documented as existing functionality here.

## 7. Reliability and Human Oversight

The Day 40 simulation reported 25% classification accuracy across four predefined candidate profiles. This small simulation is not a production accuracy benchmark, but it demonstrates that calibration gaps remain.

- Do not use scores as the sole basis for hiring.
- Retain human recruiter review.
- Validate score behavior using larger, diverse, recruiter-reviewed datasets.
- Treat keyword, confidence, and language signals as limited indicators.
- Protect candidate data and apply approved retention policies.

## 8. Related Tests

- `tests/test_day33_interview_engine.py`
- `tests/test_day37_hr_interview_scoring_engine.py`
- `tests/test_day39_interview_summary_generator.py`
- `tests/test_day40_hr_interview_simulation.py`
- `tests/test_ats_api.py`
