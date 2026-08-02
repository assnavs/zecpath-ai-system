# Shortlisting Automation Module

## Overview

The Shortlisting Automation Module is responsible for automatically classifying ranked candidates according to configurable ATS score thresholds.

After candidates have been evaluated and ranked, recruiters need to determine which applicants should move forward, which require further review, and which should be rejected.

The Shortlisting Automation Module automates this process by creating three candidate decision zones:

- Shortlisted
- Review
- Rejected

This provides a consistent and transparent mechanism for candidate filtering.

---

## Objective

The objective of the Shortlisting Automation Module is to automate candidate filtering and shortlisting using configurable ATS score thresholds.

The module is designed to:

- Load shortlisting thresholds from configuration.
- Automatically shortlist high-scoring candidates.
- Create a review zone for moderate-scoring candidates.
- Automatically reject candidates below the minimum threshold.
- Integrate with candidate ranking.
- Generate recruiter-friendly screening results.

---

## Shortlisting Threshold Configuration

The shortlisting thresholds are stored separately from the Python implementation.

Configuration file:

```text
data/shortlisting_thresholds.json
```

Current configuration:

```json
{
    "shortlist_threshold": 80,
    "review_threshold": 60,
    "top_candidate_limit": 5
}
```

Separating the thresholds from the application logic makes the system easier to configure and maintain.

---

## Candidate Decision Zones

### Shortlisted Zone

Candidates with ATS scores of **80 or above** are classified as:

```text
Shortlisted
```

These candidates demonstrate strong alignment with the evaluation criteria and can be considered for the next stage of recruitment.

---

### Review Zone

Candidates with ATS scores from **60 up to below 80** are classified as:

```text
Review
```

These candidates may possess relevant qualifications but require additional recruiter evaluation before a final decision is made.

---

### Auto-Reject Zone

Candidates scoring **below 60** are classified as:

```text
Rejected
```

This creates an automatic rejection zone for candidates who do not meet the configured minimum ATS threshold.

---

## Shortlisting Workflow

The module follows this workflow:

```text
Candidate List
      ↓
Auto-Ranking Engine
      ↓
Rank Candidates by ATS Score
      ↓
Load Threshold Configuration
      ↓
Evaluate Candidate Score
      ↓
 ┌────────────┬───────────┬───────────┐
 ↓            ↓           ↓
Shortlisted  Review     Rejected
```

This allows candidate ranking and filtering to operate as a connected automated process.

---

## Decision Logic

The system evaluates each candidate according to the configured thresholds.

The logic can be represented as:

```text
Score >= 80
    → Shortlisted

Score >= 60 and Score < 80
    → Review

Score < 60
    → Rejected
```

---

## Example Classification

The test dataset produced the following results:

| Rank | Candidate | Score | Decision |
|---:|---|---:|---|
| 1 | Candidate A | 91 | Shortlisted |
| 2 | Candidate D | 84 | Shortlisted |
| 3 | Candidate B | 78 | Review |
| 4 | Candidate E | 67 | Review |
| 5 | Candidate C | 56 | Rejected |

Therefore:

```text
Total Candidates: 5
Shortlisted: 2
Review: 2
Rejected: 1
```

---

## Configurable Design

The threshold values are not permanently hard-coded into the shortlisting logic.

Instead, they are loaded from:

```text
shortlisting_thresholds.json
```

This allows future changes to recruitment thresholds without rewriting the main shortlisting module.

For example, the organization could later increase the shortlist threshold from 80 to 85 by changing the configuration.

---

## Threshold Validation

The module verifies that the configured review threshold is not greater than the shortlist threshold.

An invalid configuration could create conflicting decision zones.

The validation mechanism prevents such configurations from being used by the system.

---

## Features

The implemented Shortlisting Automation Module supports:

- Automatic candidate shortlisting
- Configurable thresholds
- Shortlist zone
- Review zone
- Auto-reject zone
- Candidate ranking integration
- Candidate count summaries
- Top-candidate generation
- Structured recruiter-friendly output
- Logging
- Threshold validation

---

## Benefits

The shortlisting module provides:

- Faster initial candidate screening.
- Consistent application of screening rules.
- Reduced repetitive recruiter effort.
- Transparent shortlisting decisions.
- Flexible threshold configuration.
- Easy integration with ATS scoring and ranking components.

---

## Testing and Validation

The module was tested using candidates with scores across all three decision zones.

The test successfully verified:

```text
2 candidates → Shortlisted
2 candidates → Review
1 candidate  → Rejected
```

The test also confirmed that ranking information remained available after the shortlisting decisions were assigned.

All Candidate Ranking and Shortlisting tests passed successfully.

---

## Conclusion

The Shortlisting Automation Module successfully automates candidate filtering using configurable ATS score thresholds. By separating applicants into Shortlisted, Review, and Rejected zones, the module provides a transparent and efficient screening mechanism while still allowing recruiters to manually review candidates who fall within the intermediate evaluation range.