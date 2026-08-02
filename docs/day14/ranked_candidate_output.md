# Ranked Candidate Output

## Overview

The Ranked Candidate Output represents the final structured result produced by the Day 14 Candidate Ranking and Shortlisting workflow.

It combines candidate ranking information, ATS scores, shortlisting decisions, threshold information, and top-candidate results into a recruiter-friendly structured output.

The purpose of this output is to transform raw candidate scores into information that can be easily consumed by recruiters or integrated into future application interfaces.

---

## Objective

The objective of the Ranked Candidate Output is to provide a clear and structured representation of candidate screening results.

The output should allow recruiters to quickly understand:

- Total number of candidates evaluated.
- Candidate ranking.
- ATS score of each candidate.
- Shortlisting decision.
- Number of shortlisted candidates.
- Number of candidates requiring review.
- Number of rejected candidates.
- Current threshold configuration.
- Top-ranked candidates.

---

## Output Generation Workflow

The ranked output is generated after both the ranking and shortlisting processes have completed.

```text
Candidate ATS Scores
        ↓
Auto-Ranking Engine
        ↓
Ranked Candidate List
        ↓
Shortlisting Automation
        ↓
Shortlisted / Review / Rejected
        ↓
Ranked Candidate Output
```

---

## Candidate-Level Information

Each candidate record contains information such as:

```text
Candidate ID
Candidate Name
ATS Score
Rank
Decision
```

Example:

```json
{
    "candidate_id": "C001",
    "name": "Candidate A",
    "score": 91.0,
    "rank": 1,
    "decision": "Shortlisted"
}
```

This makes the output understandable without requiring the recruiter to interpret raw scoring calculations.

---

## Summary Information

The output also provides aggregate information.

For the tested candidate dataset:

```text
Total Candidates:       5
Shortlisted Candidates: 2
Review Candidates:      2
Rejected Candidates:    1
```

This provides a quick summary of the candidate pool.

---

## Threshold Information

The output includes the thresholds used during candidate classification.

Example:

```json
"thresholds": {
    "shortlist_threshold": 80,
    "review_threshold": 60
}
```

Including the threshold values improves transparency because the recruiter can understand why a particular candidate received a specific decision.

---

## Ranked Candidate List

The complete tested candidate ranking was:

| Rank | Candidate | ATS Score | Decision |
|---:|---|---:|---|
| 1 | Candidate A | 91.0 | Shortlisted |
| 2 | Candidate D | 84.0 | Shortlisted |
| 3 | Candidate B | 78.0 | Review |
| 4 | Candidate E | 67.0 | Review |
| 5 | Candidate C | 56.0 | Rejected |

The highest-scoring candidates appear first, allowing recruiters to focus immediately on the strongest applicants.

---

## Sample Structured Output

```json
{
    "total_candidates": 5,
    "shortlisted_count": 2,
    "review_count": 2,
    "rejected_count": 1,
    "thresholds": {
        "shortlist_threshold": 80,
        "review_threshold": 60
    },
    "ranked_candidates": [
        {
            "candidate_id": "C001",
            "name": "Candidate A",
            "score": 91.0,
            "rank": 1,
            "decision": "Shortlisted"
        },
        {
            "candidate_id": "C004",
            "name": "Candidate D",
            "score": 84.0,
            "rank": 2,
            "decision": "Shortlisted"
        },
        {
            "candidate_id": "C002",
            "name": "Candidate B",
            "score": 78.0,
            "rank": 3,
            "decision": "Review"
        },
        {
            "candidate_id": "C005",
            "name": "Candidate E",
            "score": 67.0,
            "rank": 4,
            "decision": "Review"
        },
        {
            "candidate_id": "C003",
            "name": "Candidate C",
            "score": 56.0,
            "rank": 5,
            "decision": "Rejected"
        }
    ]
}
```

---

## Top Candidate List

The output also supports a separate top-candidate list.

The maximum number of candidates returned is controlled through:

```text
top_candidate_limit
```

The current configuration uses:

```text
5
```

Therefore, when the test dataset contains exactly five candidates, all five candidates appear in the top-candidate list.

For a larger applicant pool, only the highest-ranked candidates up to the configured limit would be returned.

---

## Recruiter-Friendly Design

The structured output is designed to provide recruiters with the most important information without requiring them to inspect internal ATS calculations.

Recruiters can immediately identify:

- Who ranked highest.
- Which candidates were shortlisted.
- Which candidates require manual review.
- Which candidates were rejected.
- What thresholds were applied.

---

## Integration Possibilities

The structured output can later be used by:

- Recruiter dashboards
- Candidate management interfaces
- Screening APIs
- Reporting systems
- Interview selection workflows
- Candidate notification systems

Because the output uses structured data, it can be consumed easily by other application components.

---

## Features

The Ranked Candidate Output provides:

- Candidate ranking
- ATS scores
- Shortlisting decisions
- Candidate identifiers
- Summary counts
- Threshold information
- Top-candidate lists
- Structured JSON-compatible format
- Recruiter-friendly presentation

---

## Testing Result

The generated output was validated through the Day 14 unit test.

The system correctly produced:

```text
Rank 1 → Candidate A → 91 → Shortlisted
Rank 2 → Candidate D → 84 → Shortlisted
Rank 3 → Candidate B → 78 → Review
Rank 4 → Candidate E → 67 → Review
Rank 5 → Candidate C → 56 → Rejected
```

All Candidate Ranking and Shortlisting tests passed successfully.

---

## Conclusion

The Ranked Candidate Output provides a structured and recruiter-friendly representation of candidate evaluation results. By combining ranking positions, ATS scores, screening decisions, threshold information, and top-candidate lists, the output transforms candidate scoring data into actionable recruitment information and prepares the system for future dashboard and recruitment workflow integration.