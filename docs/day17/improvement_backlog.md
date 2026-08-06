# ATS Improvement Backlog

## Day 17 – Findings and Future Improvements

## 1. Overview

The Day 17 ATS System Testing activity identified areas where the resume evaluation system can be improved.

The purpose of this backlog is to convert testing observations into clear future development actions.

The current controlled evaluation achieved:

```text
Accuracy: 91.67%
Precision: 100.00%
Recall: 87.50%
F1 Score: 93.33%
```

One mismatch was identified.

---

## 2. Primary Mismatch

Test case:

```text
TC012
```

Candidate type:

```text
Non-Tech Fresher
```

Target role:

```text
Business Analyst
```

Results:

```text
ATS Score: 69.05
ATS Decision: REJECT
Manual Decision: SELECT
```

Selection threshold:

```text
70.00
```

Difference from threshold:

```text
0.95
```

The candidate was therefore rejected despite being extremely close to the selection boundary.

---

# 3. Improvement Priority 1 – Borderline Review Zone

## Problem

The current system-level evaluation converts scores directly into:

```text
SELECT
or
REJECT
```

using a fixed threshold.

A candidate scoring 69.05 is therefore rejected even though the candidate is only 0.95 points below the selection threshold.

## Proposed Improvement

Introduce a review zone around the selection threshold.

Example:

```text
Score >= 75        → SELECT
Score 65–74.99     → MANUAL REVIEW
Score < 65         → REJECT
```

The exact values should be calibrated using validation data rather than adopted without testing.

## Expected Benefit

This could reduce false-negative decisions involving borderline candidates.

### Priority

```text
HIGH
```

---

# 4. Improvement Priority 2 – Role-Specific Thresholds

## Problem

Different job roles may require different decision boundaries.

Using the same selection threshold for:

```text
Data Scientist
Frontend Developer
Backend Developer
Business Analyst
```

may not reflect differences in candidate profiles and hiring expectations.

## Proposed Improvement

Support configurable thresholds per role.

Example structure:

```text
Data Scientist      → Configurable threshold
Backend Developer   → Configurable threshold
Frontend Developer  → Configurable threshold
Business Analyst    → Configurable threshold
```

Thresholds should be selected using validated human-reviewed datasets.

### Priority

```text
HIGH
```

---

# 5. Improvement Priority 3 – Fresher-Aware Evaluation

## Problem

Fresher candidates naturally have lower professional experience scores.

An evaluation system that gives significant weight to experience can disadvantage otherwise relevant entry-level candidates.

TC012 demonstrates the importance of considering interactions between:

```text
Role Type
+
Experience Level
+
Skills
+
Education
+
Semantic Relevance
```

## Proposed Improvement

Introduce profile-aware scoring strategies for:

```text
Fresher
Junior
Mid-Level
Senior
```

For fresher roles, the system could place comparatively greater emphasis on validated skills, relevant education, projects, internships, and semantic relevance.

### Priority

```text
HIGH
```

---

# 6. Improvement Priority 4 – Expand Non-Tech Role Testing

## Observation

Non-tech category accuracy in the current controlled dataset was:

```text
66.67%
```

However, only three cases were evaluated.

## Proposed Improvement

Expand testing across additional non-tech or mixed business roles such as:

```text
Business Analyst
Operations Analyst
Marketing Analyst
HR Analyst
Business Development
Project Coordinator
```

The specific roles should reflect actual intended product use cases.

### Priority

```text
HIGH
```

---

# 7. Improvement Priority 5 – Larger Evaluation Dataset

## Problem

The current evaluation contains:

```text
12 test cases
```

This is sufficient for development testing but too small for reliable real-world performance claims.

## Proposed Improvement

Build a larger human-reviewed evaluation dataset containing:

- Multiple industries
- Different experience levels
- Technical roles
- Non-technical roles
- Career transitions
- Fresh graduates
- Senior candidates
- Different resume writing styles
- Strong and weak matches
- Borderline candidates

### Priority

```text
HIGH
```

---

# 8. Improvement Priority 6 – Human Review Labels

## Problem

Current manual decisions are controlled test labels.

Production evaluation should rely on consistently defined human review criteria.

## Proposed Improvement

Create a structured human-review rubric.

For example, reviewers could independently evaluate:

```text
Skill relevance
Experience relevance
Education relevance
Project relevance
Overall suitability
Final decision
```

Where possible, multiple reviewers could be used to measure agreement.

### Priority

```text
MEDIUM
```

---

# 9. Improvement Priority 7 – Threshold Calibration

## Problem

The current evaluation uses:

```text
70
```

as the binary selection threshold.

TC012 shows that small threshold differences can change candidate decisions.

## Proposed Improvement

Evaluate multiple candidate thresholds using a validation dataset.

For each threshold, measure:

```text
Precision
Recall
F1 Score
False Positive Rate
False Negative Rate
```

Then select thresholds according to the intended recruitment workflow and acceptable error trade-offs.

### Priority

```text
HIGH
```

---

# 10. Improvement Priority 8 – Mismatch Logging

## Proposed Improvement

Automatically record ATS/manual-review disagreements.

A mismatch record could include:

```text
Case ID
Job Role
Profile Level
ATS Score
ATS Decision
Manual Decision
Mismatch Type
```

Mismatch types:

```text
False Positive
False Negative
```

This would make future error analysis easier.

### Priority

```text
MEDIUM
```

---

# 11. Improvement Priority 9 – Category-Level Monitoring

Future evaluation should continuously calculate metrics separately for:

```text
Job Role
Experience Level
Candidate Category
```

This can help identify situations where overall accuracy appears acceptable while a specific candidate group performs poorly.

### Priority

```text
MEDIUM
```

---

# 12. Improvement Priority 10 – Regression Testing

The Day 17 test suite should become a regression baseline.

Whenever scoring weights, thresholds, normalization logic, semantic matching, or ranking behavior changes, the ATS system evaluation should be rerun.

Future versions can then compare:

```text
Previous Metrics
       ↓
Updated System
       ↓
New Metrics
       ↓
Performance Improved / Regressed
```

### Priority

```text
MEDIUM
```

---

# 13. Backlog Summary

| Improvement | Priority |
|---|---|
| Borderline review zone | High |
| Role-specific thresholds | High |
| Fresher-aware evaluation | High |
| Expand non-tech testing | High |
| Larger evaluation dataset | High |
| Human-review rubric | Medium |
| Threshold calibration | High |
| Automatic mismatch logging | Medium |
| Category-level monitoring | Medium |
| Regression testing | Medium |

---

# 14. Recommended Next Testing Direction

The next evaluation cycle should prioritize:

1. Increasing the number of non-tech test cases.
2. Adding more borderline candidates around the decision threshold.
3. Expanding fresher and entry-level evaluation.
4. Testing alternative decision thresholds.
5. Measuring whether changes improve recall without creating excessive false positives.
6. Re-running the Day 17 baseline after scoring changes.

---

# 15. Conclusion

Day 17 ATS System Testing identified one meaningful false-negative mismatch while achieving 91.67% overall accuracy on the controlled test set.

Rather than modifying the expected label to artificially obtain 100% accuracy, the mismatch has been retained as evidence for system improvement.

The most important improvement opportunities are borderline-candidate handling, role-specific calibration, fresher-aware evaluation, broader non-tech testing, and expansion of the human-reviewed validation dataset.

This backlog provides a structured basis for improving ATS reliability and role adaptability in future development cycles.