# Day 21 - Eligibility Decision Engine

## 1. Objective

The Eligibility Decision Engine automatically evaluates candidates using ATS results and recruiter-defined eligibility rules.

The engine determines whether a candidate should proceed to AI screening, require recruiter review, or be rejected.

## 2. Eligibility Parameters

The engine evaluates candidates using:

- Minimum ATS score
- Mandatory skills
- Experience range
- Location constraints
- Availability constraints

## 3. Decision Categories

### ELIGIBLE

A candidate is marked ELIGIBLE when the ATS score reaches the configured minimum threshold and the required eligibility rules are satisfied.

### REVIEW

A candidate is marked REVIEW when the candidate reaches the configured review threshold but requires further recruiter consideration.

### REJECTED

A candidate is marked REJECTED when the ATS score is below the configured review threshold.

## 4. Processing Flow

ATS Result
|
v
ATS Score Extraction
|
v
Job Role Rule Selection
|
v
Mandatory Skill Validation
|
v
Experience Validation
|
v
Location / Availability Validation
|
v
Rule + Score Evaluation
|
+-----------------------------+
|             |               |
v             v               v
ELIGIBLE     REVIEW        REJECTED

## 5. Rule Configuration

Eligibility rules are stored in:

data/eligibility_rules.json

The configuration supports job-role-specific rules including:

- Minimum ATS score
- Review score threshold
- Mandatory skills
- Minimum and maximum experience
- Location constraints
- Availability constraints

## 6. Implementation

The main implementation is located at:

scoring/eligibility_decision_engine.py

The engine loads the configured rules and evaluates each candidate against the selected job role.

## 7. ATS Integration

The Eligibility Decision Engine accepts ATS scoring results directly.

It supports:

- Direct ATS score output
- Structured ATS API responses containing the score inside the data field

This allows the eligibility layer to work with the existing ATS scoring system.

## 8. Explainable Results

The engine returns:

- Candidate ID
- Candidate name
- Job role
- ATS score
- Final eligibility decision
- Configured thresholds
- Mandatory skill results
- Experience validation result
- Location validation result
- Availability validation result

This makes the decision easier to understand and review.

## 9. Testing

The Day 21 automated test suite validates:

- Eligible candidate classification
- Review candidate classification
- Rejected candidate classification
- Mandatory skill validation
- Experience range validation
- ATS output integration

### Test Result

All Day 21 Eligibility Decision Engine tests passed successfully.

## 10. Day 21 Deliverable

The completed Eligibility Decision Engine provides a configurable rule-based eligibility layer on top of the existing ATS scoring system.

The final system can classify candidates into:

ELIGIBLE -> REVIEW -> REJECTED

