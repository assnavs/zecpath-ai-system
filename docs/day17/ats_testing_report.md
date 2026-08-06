# ATS System Testing Report

## Day 17 – ATS System Testing

## 1. Overview

The ATS System Testing activity was conducted to evaluate the accuracy, reliability, and role adaptability of the resume evaluation and scoring system.

The testing process compared ATS-generated candidate decisions against predefined manual review decisions across multiple candidate categories.

The evaluation covered:

- Technical job roles
- Non-technical job roles
- Fresher resumes
- Senior candidate profiles

A total of 12 controlled candidate test cases were evaluated.

---

## 2. Testing Objective

The primary objectives of the testing activity were to:

- Validate ATS scoring behavior.
- Evaluate candidate selection accuracy.
- Test adaptability across different job roles.
- Evaluate fresher and experienced candidate profiles.
- Compare ATS decisions against manual review decisions.
- Identify false-positive and false-negative decisions.
- Measure precision and recall.
- Identify mismatch cases.
- Create improvement recommendations based on observed results.

---

## 3. Testing Methodology

Each test case contained:

- Candidate category
- Profile level
- Target job role
- Skill match score
- Experience relevance score
- Education alignment score
- Semantic similarity score
- Manual review decision

The existing ATS Scoring Engine generated an overall candidate score.

For system-level evaluation, the following decision threshold was used:

```text
ATS Score >= 70 → SELECT
ATS Score < 70  → REJECT
```

The ATS-generated decision was then compared with the expected manual review decision.

---

## 4. Roles and Candidate Types Tested

The evaluation included the following job roles:

```text
Data Scientist
Backend Developer
Frontend Developer
Business Analyst
```

The first three represent technical roles, while Business Analyst was included to evaluate adaptability beyond purely technical roles.

Candidate profile categories included:

```text
Tech Role
Non-Tech Role
Fresher Resume
Senior Profile
```

---

## 5. Candidate Test Results

| Test Case | Category | Job Role | ATS Score | ATS Decision | Manual Decision | Result |
|---|---|---|---:|---|---|---|
| TC001 | Tech Role | Data Scientist | 89.90 | SELECT | SELECT | Match |
| TC002 | Tech Role | Backend Developer | 83.20 | SELECT | SELECT | Match |
| TC003 | Tech Role | Frontend Developer | 51.20 | REJECT | REJECT | Match |
| TC004 | Non-Tech Role | Business Analyst | 85.30 | SELECT | SELECT | Match |
| TC005 | Non-Tech Role | Business Analyst | 50.30 | REJECT | REJECT | Match |
| TC006 | Fresher Resume | Data Scientist | 74.60 | SELECT | SELECT | Match |
| TC007 | Fresher Resume | Frontend Developer | 63.70 | REJECT | REJECT | Match |
| TC008 | Fresher Resume | Backend Developer | 75.30 | SELECT | SELECT | Match |
| TC009 | Senior Profile | Data Scientist | 92.90 | SELECT | SELECT | Match |
| TC010 | Senior Profile | Backend Developer | 90.55 | SELECT | SELECT | Match |
| TC011 | Senior Profile | Frontend Developer | 68.40 | REJECT | REJECT | Match |
| TC012 | Non-Tech Role / Fresher | Business Analyst | 69.05 | REJECT | SELECT | Mismatch |

Out of 12 test cases, 11 ATS decisions matched the expected manual review decisions.

One mismatch was identified.

---

## 6. Overall Test Results

The system produced the following results:

```text
Total Test Cases:       12
Correct Predictions:    11
Incorrect Predictions:   1

Accuracy:               91.67%
Precision:             100.00%
Recall:                 87.50%
F1 Score:               93.33%

False Positives:         0
False Negatives:         1
Mismatch Cases:          1
```

---

## 7. Category-Level Results

### Tech Roles

```text
Total Cases: 3
Correct Predictions: 3
Accuracy: 100.00%
```

The tested technical profiles were correctly classified within the controlled dataset.

---

### Non-Tech Roles

```text
Total Cases: 3
Correct Predictions: 2
Accuracy: 66.67%
```

One mismatch occurred within the non-tech candidate group.

This indicates an area requiring additional testing and possible role-specific calibration.

---

### Fresher Resumes

```text
Total Cases: 3
Correct Predictions: 3
Accuracy: 100.00%
```

The three dedicated fresher test cases were classified correctly.

However, TC012 also represents a fresher Business Analyst profile and exposed a boundary-condition issue when fresher characteristics were combined with a non-tech role.

---

### Senior Profiles

```text
Total Cases: 3
Correct Predictions: 3
Accuracy: 100.00%
```

The tested senior candidate profiles were correctly classified.

---

## 8. Mismatch Analysis

One mismatch was identified:

```text
Test Case: TC012
Candidate: Non-Tech Fresher
Job Role: Business Analyst

ATS Score: 69.05
ATS Decision: REJECT
Manual Decision: SELECT
```

The configured system-level selection threshold was:

```text
70.00
```

The candidate's score was only:

```text
0.95 points
```

below this threshold.

This represents a near-threshold false-negative case.

The result suggests that a strict binary decision threshold may not adequately represent borderline candidates, particularly where fresher candidates have strong education, skills, or semantic relevance but limited professional experience.

---

## 9. Reliability Observation

The ATS correctly classified 11 of the 12 controlled test cases.

No false-positive candidate selections occurred.

The single error was a false negative, meaning the system rejected a candidate that manual review considered selectable.

This is reflected in:

```text
Precision: 100.00%
Recall: 87.50%
```

The high precision indicates that all candidates predicted as SELECT in this test set were also marked SELECT by manual review.

The lower recall reflects the missed selectable candidate in TC012.

---

## 10. Role Adaptability Observation

The ATS successfully processed technical and non-technical role configurations.

Technical-role test cases performed consistently in the controlled dataset.

The Business Analyst tests exposed one mismatch, indicating that non-technical role configuration may benefit from further calibration and broader evaluation data.

The result should not be interpreted as a general real-world accuracy rate because each category currently contains only a small controlled test sample.

---

## 11. Key Findings

The Day 17 evaluation identified the following:

- ATS scoring executed reliably across all 12 test cases.
- Technical roles were handled successfully in the controlled test set.
- Senior profiles were classified correctly.
- Dedicated fresher test cases were classified correctly.
- Non-tech role support is functional.
- One false-negative mismatch was detected.
- No false positives were detected.
- Borderline scores require special attention.
- Role-specific threshold calibration could improve adaptability.
- Additional real-world testing data will be required before production-level accuracy claims can be made.

---

## 12. Testing Conclusion

The ATS System Testing activity was completed successfully.

The system achieved 91.67% accuracy, 100.00% precision, 87.50% recall, and a 93.33% F1 score across the 12 controlled test cases.

The evaluation also successfully identified one meaningful mismatch involving a fresher Business Analyst candidate near the selection threshold.

The mismatch provides a useful basis for future improvements involving borderline-candidate handling, role-specific calibration, and broader validation datasets.

The results demonstrate that the ATS testing framework can systematically compare automated decisions against manual review and track measurable accuracy and mismatch indicators.