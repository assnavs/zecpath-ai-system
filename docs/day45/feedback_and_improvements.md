\# Day 45 — Feedback and Improvement Plan



\## 1. Objective



This document records the findings from the existing HR Interview Simulation System and identifies improvements for future development.



\## 2. Existing Benchmark Results



| Metric | Result |

|---|---:|

| Candidate profiles simulated | 4 |

| Classification agreement | 25% |

| Classification matches | 1 out of 4 |

| Interview Mean Absolute Error | 16.79 |

| Aptitude Mean Absolute Error | 15.35 |



The results show differences between AI-generated scores and predefined reference evaluations. These reference values are not ground truth.



\## 3. Identified Limitations



\### 3.1 Scoring Calibration



Some AI-generated classifications differ from the reference classifications. Scoring thresholds and weights need evaluation against a larger, independently reviewed dataset.



\### 3.2 Limited Test Data



The current benchmark uses only four predefined candidate profiles. It does not represent the full diversity of candidates, job roles, experience levels, or communication styles.



\### 3.3 Keyword-Based Evaluation



Keyword-based matching may not recognize semantically similar answers expressed using different vocabulary. Short answers may also provide insufficient evidence for reliable aptitude evaluation.



\### 3.4 Recommendation Reliability



Generated recommendations may appear more definitive than the supporting evidence justifies. Recruiters should review the score breakdown, limitations, and relevant evidence.



\### 3.5 Fairness and Accessibility



Language fluency, communication differences, accessibility needs, and cultural expression may affect some evaluation signals. These are risks requiring further investigation, not proven findings from the current benchmark.



\## 4. Prioritized Improvement Plan



| Priority | Improvement | Verification |

|---|---|---|

| P0 | Keep human recruiters responsible for hiring decisions | Confirm recommendations are advisory |

| P0 | Expand recruiter-reviewed benchmark data | Evaluate on a representative dataset |

| P1 | Calibrate scoring weights and thresholds | Test against independent reference evaluations |

| P1 | Improve semantic answer evaluation | Test paraphrases and different answer styles |

| P1 | Expand aptitude scenarios | Use diverse, job-relevant questions |

| P1 | Investigate fairness and accessibility | Conduct an appropriate, privacy-protective evaluation |

| P2 | Improve explanations and auditability | Record configuration versions and evaluation evidence |

| P2 | Strengthen regression testing | Track errors and failure cases across releases |



\## 5. Recommended Validation Process



1\. Define job-related competencies and scoring rubrics.

2\. Collect appropriately authorized and representative evaluation data.

3\. Have qualified reviewers evaluate answers independently.

4\. Document how disagreements are resolved.

5\. Separate calibration data from held-out test data.

6\. Measure score errors, classification agreement, and relevant fairness indicators.

7\. Record the software and configuration versions used.

8\. Define acceptance criteria before testing.

9\. Repeat validation after significant scoring changes.

10\. Do not deploy automated hiring decisions based solely on AI-generated scores.



\## 6. Future Success Criteria



Future experiments should aim to reduce held-out score errors, improve agreement with independently reviewed evaluations, maintain stable results across representative scenarios, and document failure handling.



These are proposed goals, not achieved results.



\## 7. Conclusion



The current simulation is useful for demonstrating system integration and identifying calibration gaps. Larger-scale validation, transparent reporting, privacy safeguards, and accountable human review are necessary before considering real-world recruitment use.
