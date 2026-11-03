# Day 50 – Machine Test AI Framework

## Objective
Evaluate coding, debugging, file-based and mini system-design tasks.

## Implementation
- Module: `interview_ai/machine_test_engine.py`
- Metrics: correctness, efficiency, code quality and problem-solving approach.
- Correctness can be calculated from externally supplied test counts.
- Efficiency compares elapsed time with a task time limit.
- Reports retain code-snapshot and execution-result metadata.
- Task-type-specific weights and session aggregation are supported.

## Safety and limitations
This engine does not execute candidate code. Test outputs and rubric scores must come from a trusted external runner/reviewer. A production sandbox needs isolation, resource limits, network restrictions, filesystem controls and security review. Human review remains required.
