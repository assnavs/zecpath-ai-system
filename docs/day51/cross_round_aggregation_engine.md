# Day 51 – Cross-Round Aggregation Engine

## Objective
Combine ATS, screening, HR interview, technical interview and machine-test scores into one hiring-fit score.

## Implementation
- Role-specific weights are provided for roles already represented in the project and related developer roles.
- Validate scores on a 0–100 scale.
- Missing rounds are excluded; remaining weights are renormalized.
- Return per-round configured/effective weights, missing rounds and coverage.

## Limitation
The engine consumes upstream scores; it does not invent missing values or call upstream systems. Initial weights require business validation.
