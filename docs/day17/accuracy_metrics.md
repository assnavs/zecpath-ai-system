# ATS Accuracy Metrics

## Day 17 – ATS System Evaluation

## 1. Purpose

This document summarizes the quantitative evaluation metrics generated during Day 17 ATS System Testing.

The ATS-generated candidate decisions were compared against predefined manual review decisions across 12 controlled test cases.

The evaluation measures:

- Accuracy
- Precision
- Recall
- F1 Score
- True Positives
- True Negatives
- False Positives
- False Negatives
- Mismatch count
- Category-level accuracy

---

## 2. Evaluation Dataset

Total test cases:

```text
12
```

Candidate categories:

```text
Tech Role
Non-Tech Role
Fresher Resume
Senior Profile
```

Job roles tested:

```text
Data Scientist
Backend Developer
Frontend Developer
Business Analyst
```

---

## 3. Decision Rule

For the Day 17 evaluation, ATS scores were converted into binary decisions using:

```text
Score >= 70 → SELECT
Score < 70  → REJECT
```

The positive class used for precision and recall calculation was:

```text
SELECT
```

---

## 4. Confusion Matrix Results

The evaluation produced:

```text
True Positive  (TP): 7
True Negative  (TN): 4
False Positive (FP): 0
False Negative (FN): 1
```

Confusion matrix:

|  | Manual SELECT | Manual REJECT |
|---|---:|---:|
| ATS SELECT | 7 | 0 |
| ATS REJECT | 1 | 4 |

---

## 5. Accuracy

Accuracy measures the percentage of all candidate decisions that matched manual review.

Formula:

```text
Accuracy = (TP + TN) / Total Cases
```

Calculation:

```text
Accuracy = (7 + 4) / 12

Accuracy = 11 / 12

Accuracy = 91.67%
```

### Result

```text
91.67%
```

---

## 6. Precision

Precision measures how often candidates selected by the ATS were also selected by manual review.

Formula:

```text
Precision = TP / (TP + FP)
```

Calculation:

```text
Precision = 7 / (7 + 0)

Precision = 100.00%
```

### Result

```text
100.00%
```

No false-positive selections occurred in the controlled test set.

---

## 7. Recall

Recall measures how many manually selectable candidates were successfully identified by the ATS.

Formula:

```text
Recall = TP / (TP + FN)
```

Calculation:

```text
Recall = 7 / (7 + 1)

Recall = 87.50%
```

### Result

```text
87.50%
```

The reduction from 100% recall was caused by one false-negative candidate.

---

## 8. F1 Score

The F1 Score balances precision and recall.

Formula:

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

Using:

```text
Precision = 1.00
Recall = 0.875
```

produced:

```text
F1 Score = 93.33%
```

### Result

```text
93.33%
```

---

## 9. Overall Metric Summary

| Metric | Result |
|---|---:|
| Total Cases | 12 |
| Correct Predictions | 11 |
| Incorrect Predictions | 1 |
| True Positives | 7 |
| True Negatives | 4 |
| False Positives | 0 |
| False Negatives | 1 |
| Accuracy | 91.67% |
| Precision | 100.00% |
| Recall | 87.50% |
| F1 Score | 93.33% |
| Mismatch Count | 1 |

---

## 10. Category Accuracy

### Tech Role

```text
Cases: 3
Correct: 3
Accuracy: 100.00%
```

### Non-Tech Role

```text
Cases: 3
Correct: 2
Accuracy: 66.67%
```

### Fresher Resume

```text
Cases: 3
Correct: 3
Accuracy: 100.00%
```

### Senior Profile

```text
Cases: 3
Correct: 3
Accuracy: 100.00%
```

Summary:

| Category | Cases | Correct | Accuracy |
|---|---:|---:|---:|
| Tech Role | 3 | 3 | 100.00% |
| Non-Tech Role | 3 | 2 | 66.67% |
| Fresher Resume | 3 | 3 | 100.00% |
| Senior Profile | 3 | 3 | 100.00% |

---

## 11. Mismatch Metric

Only one mismatch occurred:

```text
TC012

Role: Business Analyst
Profile: Non-Tech Fresher

ATS Score: 69.05
ATS Decision: REJECT

Manual Decision: SELECT
```

Mismatch rate:

```text
1 / 12 × 100 = 8.33%
```

Therefore:

```text
Match Rate: 91.67%
Mismatch Rate: 8.33%
```

---

## 12. Metric Interpretation

### Precision – 100%

The ATS did not incorrectly select any manually rejected candidate in this controlled dataset.

### Recall – 87.50%

The ATS missed one candidate that manual review considered selectable.

### Accuracy – 91.67%

Eleven of twelve ATS decisions matched manual decisions.

### F1 Score – 93.33%

The combined precision and recall performance remained high within the controlled evaluation set.

---

## 13. Limitations

These metrics were calculated from a small controlled dataset containing 12 test cases.

Therefore, the results are useful for:

- Development validation
- Regression testing
- Detecting scoring problems
- Identifying mismatch patterns
- Comparing future system versions

They should not yet be interpreted as statistically representative real-world recruitment performance.

A larger and more diverse human-reviewed dataset would be required for production-level accuracy evaluation.

---

## 14. Conclusion

The Day 17 ATS evaluation achieved:

```text
Accuracy:  91.67%
Precision: 100.00%
Recall:    87.50%
F1 Score:  93.33%
```

The metrics demonstrate consistent behavior across the majority of the controlled test cases while identifying one false-negative boundary case.

The measurable results provide a baseline that can be used to compare future improvements to the ATS scoring and decision framework.