# Day 30 – AI Screening System Evaluation & Performance Baseline

## 1. Objective

Day 30 focuses on evaluating the existing AI screening system and establishing a baseline for system correctness and performance.

The evaluation covers the existing ATS, screening, semantic matching, resume processing, and related components without replacing or restructuring the existing architecture.

The purpose of this baseline is to verify that the current system remains functional and to record its existing performance characteristics.

## 2. Evaluation Areas

The Day 30 evaluation covered:

- Existing ATS evaluation
- Full system test suite
- ATS performance optimization tests
- Semantic matching engine review
- Resume text cleaning
- Resume section classification
- Resume normalization
- PDF text extraction
- Semantic model reuse
- Semantic similarity processing
- Memory stability

## 3. ATS System Baseline

The existing ATS system evaluation was executed using the project test suite.

Command used:

python -m pytest tests/test_ats_system_evaluation.py -q

Result:

1 passed

A Pytest warning was reported because the existing test function returns a dictionary instead of using assertions exclusively. This warning does not cause the test to fail.

## 4. Full System Baseline

The complete existing test suite was executed.

Command used:

python -m pytest tests -q

Result:

114 passed

Warnings:

- Starlette/httpx deprecation warning
- PytestReturnNotNoneWarning in the ATS system evaluation test

The complete test suite successfully passed.

## 5. Performance Baseline

The existing ATS performance optimization test was executed.

Command used:

python -m pytest tests/test_ats_performance_optimization.py -q

Result:

1 passed in 16.01 seconds

The performance test completed successfully.

## 6. Detailed Performance Results

The performance test was executed with detailed output.

Command used:

python -m pytest tests/test_ats_performance_optimization.py -s -q

The observed measurements were:

| Metric | Result |
|---|---:|
| Text cleaning time | 0.000053 sec |
| PDF extraction time | 0.007750 sec |
| Semantic processing time | 0.055850 sec |
| Second model initialization | 0.001163 sec |
| Peak tracked memory | 0.0026 MB |

The complete performance test passed successfully.

## 7. Resume Processing Validation

The performance baseline validated existing resume-processing capabilities.

The following operations passed:

- Noisy resume text cleaning
- Profile/header detection
- Resume normalization
- PDF extraction

The section classifier successfully identified profile information such as candidate name and designation.

## 8. Semantic Matching Validation

The existing Semantic Matching Engine was reviewed as part of the Day 30 evaluation.

Implementation:

scoring/semantic_matching_engine.py

The engine uses:

- SentenceTransformer
- all-MiniLM-L6-v2
- Normalized embeddings
- Dot-product similarity
- Batch embedding generation
- Configured similarity thresholds

The engine also reuses a shared model between engine instances.

The test confirmed:

Semantic model reuse: PASSED

The second engine initialization was measured at approximately:

0.001163 seconds

This indicates that the existing shared-model optimization is functioning correctly.

## 9. Semantic Processing

The semantic matching performance test successfully calculated similarity across:

- Skills
- Experience
- Projects

The semantic processing operation completed in approximately:

0.055850 seconds

The resulting overall similarity remained within the expected 0–100 range.

## 10. Memory Stability

The performance test repeatedly executed resume text cleaning and section classification operations.

The memory stability test passed successfully.

Observed peak tracked memory:

0.0026 MB

This measurement represents the memory tracked by the test during the repeated operations.

## 11. Existing Architecture

Day 30 does not replace existing system components.

The evaluation works with the existing architecture, including:

- Resume parsing
- Text cleaning
- Resume normalization
- Resume section classification
- ATS scoring
- Semantic matching
- Screening scoring
- Candidate ranking
- Eligibility evaluation
- Fairness evaluation
- Communication signal evaluation
- Conversation flow
- Screening report generation

The purpose of Day 30 is evaluation and baseline measurement rather than architectural replacement.

## 12. Warnings Observed

Two warnings were reported during the full system test.

### 12.1 Starlette/httpx Warning

A deprecation warning was reported regarding the use of httpx with the Starlette test client.

This warning did not cause test failure.

### 12.2 Pytest Return Warning

The ATS system evaluation test returned a dictionary from the test function.

Pytest reported:

PytestReturnNotNoneWarning

This is a test-code quality warning and did not affect the successful test result.

## 13. Baseline Summary

The Day 30 baseline established the following results:

| Evaluation | Result |
|---|---|
| ATS system evaluation | 1 passed |
| Full system test suite | 114 passed |
| Performance optimization test | 1 passed |
| Detailed performance test | Passed |
| Semantic model reuse | Passed |
| Resume processing validation | Passed |
| Memory stability test | Passed |

## 14. Test Result

All Day 30 baseline evaluations completed successfully.

The complete system test suite produced:

114 passed, 2 warnings

The performance optimization test produced:

1 passed

The detailed performance evaluation also completed successfully.

## 15. Day 30 Deliverable

Day 30 establishes a verified baseline for the existing AI screening system.

The evaluation confirms that the current system components and optimization mechanisms are functioning successfully.

The baseline records:

- System test status
- ATS evaluation status
- Resume processing performance
- PDF extraction performance
- Semantic processing performance
- Semantic model reuse
- Memory stability
- Existing test warnings

No architectural replacement was performed during the Day 30 baseline evaluation.
