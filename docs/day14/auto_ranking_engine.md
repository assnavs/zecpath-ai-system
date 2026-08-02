# Auto-Ranking Engine

## Overview

The Auto-Ranking Engine is a candidate evaluation component developed as part of the Zecpath AI resume screening system. Its primary responsibility is to automatically organize candidates according to their ATS scores and assign a clear ranking position.

After candidates are evaluated by the ATS Scoring Engine, multiple candidate scores need to be compared to identify the strongest applicants. The Auto-Ranking Engine performs this process automatically by sorting candidate records from the highest score to the lowest score.

This reduces the need for recruiters to manually compare candidate scores and provides a structured ranking that can be used by the subsequent shortlisting process.

---

## Objective

The objective of the Auto-Ranking Engine is to automate candidate ranking based on ATS evaluation scores.

The module is designed to:

- Accept multiple candidate records.
- Read the ATS score associated with each candidate.
- Sort candidates in descending order of score.
- Assign sequential ranking positions.
- Handle missing or invalid scores safely.
- Generate structured ranking output.
- Support generation of top-candidate lists.

---

## Input Structure

The ranking engine receives a list of candidate records.

Each candidate record can contain information such as:

- Candidate ID
- Candidate name
- ATS score

Example input:

```json
[
    {
        "candidate_id": "C001",
        "name": "Candidate A",
        "score": 91
    },
    {
        "candidate_id": "C002",
        "name": "Candidate B",
        "score": 78
    },
    {
        "candidate_id": "C003",
        "name": "Candidate C",
        "score": 56
    }
]
```

---

## Ranking Process

The Auto-Ranking Engine follows the process below:

1. Receive the candidate list.
2. Read the ATS score for each candidate.
3. Normalize the candidate scores.
4. Handle missing or invalid score values.
5. Sort candidates from highest score to lowest score.
6. Assign ranking positions beginning from Rank 1.
7. Return the structured ranked candidate list.

The candidate with the highest ATS score receives Rank 1.

---

## Score Validation

Candidate scores are expected to fall between 0 and 100.

The implementation handles invalid values safely.

If a candidate score is missing, the value is treated as:

```text
0
```

If the score cannot be converted to a numeric value, it is also treated as 0.

Scores outside the valid ATS range are restricted to the range:

```text
0 – 100
```

This prevents invalid candidate information from causing errors during ranking.

---

## Sorting Logic

Candidates are sorted according to their ATS scores in descending order.

Example:

```text
Candidate A → 91
Candidate D → 84
Candidate B → 78
Candidate E → 67
Candidate C → 56
```

The resulting ranking becomes:

| Rank | Candidate | ATS Score |
|---:|---|---:|
| 1 | Candidate A | 91 |
| 2 | Candidate D | 84 |
| 3 | Candidate B | 78 |
| 4 | Candidate E | 67 |
| 5 | Candidate C | 56 |

This enables recruiters to immediately identify the candidates with the strongest ATS evaluation results.

---

## Ranking Position

After sorting, each candidate receives a sequential rank.

The highest-scoring candidate receives:

```text
Rank 1
```

The next candidate receives:

```text
Rank 2
```

and the process continues until every candidate has been assigned a ranking position.

---

## Top Candidate Generation

The Auto-Ranking Engine also supports retrieving a limited number of top-ranked candidates.

For example, if the configured limit is:

```text
5
```

the system can return the five highest-ranked candidates.

This functionality can be useful when recruiters need to focus only on the strongest candidates from a large applicant pool.

---

## Sample Ranked Output

```json
{
    "total_candidates": 5,
    "ranked_candidates": [
        {
            "candidate_id": "C001",
            "name": "Candidate A",
            "score": 91.0,
            "rank": 1
        },
        {
            "candidate_id": "C004",
            "name": "Candidate D",
            "score": 84.0,
            "rank": 2
        },
        {
            "candidate_id": "C002",
            "name": "Candidate B",
            "score": 78.0,
            "rank": 3
        }
    ]
}
```

---

## Features

The implemented Auto-Ranking Engine provides:

- Automatic candidate ranking
- Descending score-based sorting
- Sequential ranking positions
- ATS score normalization
- Missing score handling
- Invalid score handling
- Structured JSON-compatible output
- Top-candidate generation
- Logging support
- Integration with the shortlisting module

---

## Advantages

The Auto-Ranking Engine provides several benefits:

- Reduces manual candidate comparison.
- Creates consistent candidate rankings.
- Makes high-performing candidates easier to identify.
- Supports automated recruitment workflows.
- Handles large candidate lists efficiently.
- Produces structured data for downstream screening processes.

---

## Testing and Validation

The ranking engine was validated using five candidate records containing different ATS scores.

The test confirmed that the candidates were correctly ordered as:

```text
91 → 84 → 78 → 67 → 56
```

The candidate with a score of 91 received Rank 1, while the candidate with a score of 56 received Rank 5.

The ranking tests completed successfully.

---

## Conclusion

The Auto-Ranking Engine successfully automates the process of organizing candidates according to their ATS evaluation scores. By sorting applicants from highest to lowest score, assigning ranking positions, handling invalid data, and supporting top-candidate generation, the module provides a reliable foundation for automated candidate shortlisting and recruiter-focused candidate evaluation.