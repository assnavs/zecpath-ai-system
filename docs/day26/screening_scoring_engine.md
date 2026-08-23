# Day 26 – Screening Scoring Engine

## 1. Objective

The Screening Scoring Engine evaluates candidate responses from the screening workflow using multiple assessment criteria.

The engine calculates structured screening scores based on:

- Clarity
- Relevance
- Completeness
- Consistency

The scoring system converts individual criterion scores into normalized values and produces an explainable final screening score.

## 2. Processing Capabilities

The Day 26 Screening Scoring Engine supports:

- Screening response scoring
- Clarity evaluation
- Relevance evaluation
- Completeness evaluation
- Consistency evaluation
- Score normalization
- Score boundary handling
- Per-question scoring
- Multiple-question screening evaluation
- Final screening score calculation
- Explainable scoring output
- Empty screening handling

## 3. Screening Scoring Flow

Candidate Screening Response
        |
        v
Criterion Scores
        |
        +-----------------------------+
        |             |               |
        v             v               v
     Clarity       Relevance    Completeness
        |             |               |
        +-------------+---------------+
                      |
                      v
                 Consistency
                      |
                      v
              Score Normalization
                      |
                      v
                Weighted Score
                      |
                      v
             Final Screening Score

## 4. Scoring Criteria

The engine evaluates four primary criteria:

### Clarity

Measures how clearly the candidate communicates the answer.

### Relevance

Measures how closely the response addresses the screening question.

### Completeness

Measures whether the candidate provides sufficient information in the response.

### Consistency

Measures the consistency and reliability of the candidate's response.

## 5. Score Normalization

Individual criterion scores are accepted on a 0–10 scale.

The engine normalizes these values into a 0–100 scale before applying the configured criterion weights.

Scores outside the supported range are safely constrained to the valid range.

Examples:

- 0 → 0
- 5 → 50
- 10 → 100

## 6. Per-Question Scoring

The engine provides a score_question() method for evaluating an individual screening response.

The result contains:

- Question ID
- Individual criterion scores
- Normalized weighted score
- Score-weight explanation

This provides an explainable representation of how each screening response was evaluated.

## 7. Multiple-Question Scoring

The score_screening() method accepts multiple screening responses.

Each response is evaluated individually before being combined into the final screening result.

The final screening score represents the average of the normalized per-question scores.

## 8. Structured Output

The final screening result contains:

- Total number of questions
- Final screening score
- Individual question scores
- Explanation of the final score calculation

This structured output can be used by downstream screening and candidate evaluation components.

## 9. Empty Screening Handling

If no screening responses are provided, the engine safely returns:

- Total questions: 0
- Final screening score: 0.0
- Empty question-score list
- Explanation indicating that no responses were provided

## 10. Explainability

The scoring engine provides weight information for each criterion:

- Clarity weight
- Relevance weight
- Completeness weight
- Consistency weight

This allows downstream components to understand how the final score was produced.

## 11. Implementation

Main implementation:

scoring/screening_scoring_engine.py

Configuration:

data/screening_scoring_configuration.json

Automated tests:

tests/test_screening_scoring_engine.py

## 12. Testing

The Day 26 automated test suite validates:

- Configuration file availability
- Score normalization
- Score boundary handling
- Individual question scoring
- Perfect score calculation
- Multiple-question scoring
- Perfect screening evaluation
- Empty screening handling
- Explainable scoring output

## Test Result

All Day 26 Screening Scoring Engine tests passed successfully.

9 passed in 0.09s

## 13. Day 26 Deliverable

The completed Screening Scoring Engine provides a structured and explainable scoring layer for candidate screening.

The engine can evaluate individual screening responses, aggregate multiple responses, normalize scores, and produce a final screening score suitable for downstream candidate evaluation.
