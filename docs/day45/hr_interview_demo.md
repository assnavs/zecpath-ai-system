\## Day 45 — HR Interview Demo



\## 1. Objective



The objective of Day 45 is to demonstrate the existing HR Interview Simulation System, explain the scoring breakdown, review hiring recommendations, document improvements based on feedback, and prepare the system for handover.



\## 2. System Workflow



The system follows this workflow:



1\. Candidate profile selection.

2\. Interview session simulation.

3\. Candidate answer evaluation.

4\. Adaptive follow-up question analysis.

5\. Interview scoring.

6\. Aptitude evaluation.

7\. Summary and recommendation generation.

8\. Comparison with predefined reference evaluations.

9\. Identification of scoring inconsistencies.

10\. Documentation of improvements and limitations.



\## 3. Candidate Demonstration



The existing simulation engine defines four candidate profiles.



| Candidate | Profile Type |

|---|---|

| Ananya Menon | Confident |

| Rahul Nair | Hesitant |

| Arjun Kumar | Inexperienced |

| Meera Thomas | Overqualified |



These are demonstration profiles, not actual candidate assessments.



\## 4. Recorded Simulation Results



| Candidate | Interview Score | Interview Level | Aptitude Score | Recommendation |

|---|---:|---|---:|---|

| Ananya Menon | 75.32 | Good | 67.46 | Recommended |

| Rahul Nair | 72.41 | Good | 45.30 | Consider with Review |

| Arjun Kumar | 81.64 | Excellent | 62.61 | Recommended |

| Meera Thomas | 78.41 | Good | 62.44 | Recommended |



These results are from the existing benchmark report. Run the simulation again to obtain fresh results when needed.



\## 5. Interview Scoring Breakdown



The configured scoring weights are:



| Scoring Dimension | Weight |

|---|---:|

| Answer Relevance | 35% |

| Communication | 25% |

| Confidence | 25% |

| Consistency | 15% |



The configured score range is 0–100.



Classification thresholds:



\- Excellent: 80 and above

\- Good: 65 and above

\- Moderate: 50 and above



\## 6. Benchmark Findings



The existing four-profile benchmark reported:



\- Classification agreement: 25%.

\- Interview Mean Absolute Error (MAE): 16.79.

\- Aptitude Mean Absolute Error (MAE): 15.35.



These figures describe a small predefined benchmark only. They do not establish production accuracy or prove that the system is ready for autonomous hiring decisions.



\## 7. Responsible Interpretation



\- Scores should support, not replace, human recruiter review.

\- The four profiles are demonstration profiles, not real candidate assessments.

\- Recommendations require contextual review; a score alone should not determine hiring outcomes.

\- Changes to scoring weights or thresholds should be validated with relevant tests and representative evaluation data.
