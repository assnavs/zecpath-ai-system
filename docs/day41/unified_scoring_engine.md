# Day 41 — Unified Scoring Engine

## Objective

Develop a unified scoring engine that combines ATS, screening, and HR interview scores into a structured candidate evaluation object.

## Implementation

Main module: `scoring/unified_scoring_engine.py`

Configuration: `data/unified_scoring_configuration.json`

Sample output: `data/sample_unified_candidate_score.json`

Tests: `tests/test_day41_unified_scoring_engine.py`

The engine consumes existing round scores rather than recalculating the internal metrics of the existing scoring modules.

## Cross-Round Scoring

The default weights are:

| Evaluation round | Weight |
|---|---:|
| ATS | 35% |
| Screening | 25% |
| HR interview | 40% |

Role-specific profiles are configured for Data Scientist, Data Analyst, Business Analyst, Frontend Developer, and Backend Developer.

The unified score is the weighted average of the available round scores. When a score is missing, the engine records the missing round and renormalizes the weights of the available rounds. Candidates with missing rounds should be reviewed carefully before comparing their scores.

## Hiring-Fit Calculator

The engine returns a normalized score from 0 to 100 and exposes it as `hiring_fit_percentage`. This is a weighted evaluation score, not a statistically validated probability of hiring success.

Classification thresholds are configurable:

- Excellent: 80 and above
- Good: 65 to below 80
- Moderate: 50 to below 65
- Needs improvement: below 50

## Unified Candidate Score Object

The output includes:

- Candidate ID and job role
- Individual available round scores
- Missing evaluation rounds
- Configured role weights
- Applied weights after normalization
- Unified score and hiring-fit percentage
- Classification and score range
- Weighting explanation and decision-support note

## Validation and Edge Cases

The dedicated tests cover:

- Correct weighted calculations
- Role-based weight profiles
- Missing round scores
- No available scores
- Invalid, non-numeric, non-finite, and out-of-range scores
- Score boundaries
- Unsupported roles and empty identifiers
- Invalid weights and required output fields

## Test Results

Day 41 dedicated tests: 20 passed.

Full project regression suite: 254 passed, 2 warnings.

The warnings concern the existing Starlette test-client dependency and an existing ATS evaluation test returning a dictionary. No test failures were reported.

## Limitations

The configured weights and thresholds are initial design choices, not empirically validated hiring criteria. Role-specific weights should be calibrated using a larger, recruiter-reviewed dataset. Missing-round renormalization can affect comparability between candidates. The engine is intended to support human review, not make automatic hiring decisions.