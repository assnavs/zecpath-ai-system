# Day 47 – Technical Skill Scoring Model

## Objective
Score technical answers using accuracy, depth, logical reasoning and real-world applicability.

## Implementation
- Module: `scoring/technical_skill_scoring_engine.py`
- Rubrics support coding, debugging, conceptual, scenario and system-design questions.
- Expected-concept coverage informs accuracy. Transparent answer markers inform depth, reasoning and applicability.
- Reviewer-supplied dimension scores can override heuristic estimates.
- Difficulty normalization uses reference anchors (basic 60, intermediate 65, advanced 70) mapped to a common 60-point reference.
- Reports include raw/normalized scores, skill breakdown, explanations and shallow/developing/deep labels.

## Limitations
This is a rule-based baseline, not semantic verification or a validated hiring assessment. Keyword matching can miss context and synonyms. Human review is required.
