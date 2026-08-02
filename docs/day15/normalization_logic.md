# Normalization Logic

## Overview

The Normalization Logic standardizes resume information and candidate evaluation scores before they are processed by downstream screening components.

Candidate resumes can contain inconsistent capitalization, spacing, repeated information, different data representations, and non-essential personal information.

Without normalization, these inconsistencies may negatively affect candidate comparison and automated evaluation.

The Day 15 Resume Normalizer provides a consistent preprocessing layer for structured candidate information.

---

## Objective

The primary objective of resume normalization is to transform candidate information into a consistent representation before evaluation.

The normalization process is designed to:

- Standardize resume text.
- Remove unnecessary whitespace.
- Standardize capitalization.
- Normalize skill lists.
- Remove duplicate list entries.
- Mask configured personal attributes.
- Prepare structured information for candidate evaluation.

---

## Resume Normalization Workflow

The normalization process follows this general workflow:

```text
Structured Resume
       ↓
Normalize Field Names
       ↓
Mask Configured Personal Attributes
       ↓
Normalize Text
       ↓
Normalize Lists
       ↓
Remove Duplicate Values
       ↓
Standardized Resume Output
```

---

## Field Name Normalization

Resume dictionary keys are converted into a consistent format.

For example:

```text
NAME → name
Email → email
SKILLS → skills
```

This reduces inconsistencies caused by different capitalization styles.

---

## Text Normalization

Text values are standardized using the Resume Normalizer.

The process includes:

1. Converting the input into text when required.
2. Removing repeated whitespace.
3. Removing unnecessary leading and trailing spaces.
4. Converting text to lowercase.

Example input:

```text
"  DATA   SCIENTIST with experience in Machine Learning  "
```

Normalized output:

```text
"data scientist with experience in machine learning"
```

---

## Whitespace Normalization

Resumes frequently contain inconsistent spacing caused by formatting or extraction from PDF and DOCX documents.

For example:

```text
DATA     SCIENTIST
```

is standardized to:

```text
data scientist
```

This creates a cleaner representation for downstream processing.

---

## List Normalization

Resume information such as skills may be represented as lists.

Example input:

```json
[
    "PYTHON",
    " SQL ",
    "Machine Learning",
    "python"
]
```

The normalization process:

- Converts values to lowercase.
- Removes unnecessary whitespace.
- Removes empty values.
- Removes duplicates.

Normalized result:

```json
[
    "python",
    "sql",
    "machine learning"
]
```

---

## Duplicate Removal

Duplicate information can cause certain skills or terms to appear more important simply because they occur multiple times.

The normalization module therefore removes duplicate list entries after normalization.

For example:

```text
Python
PYTHON
python
```

becomes:

```text
python
```

This produces a cleaner structured representation.

---

## Personal Attribute Masking

The normalization layer also masks configured non-essential personal attributes.

Configured examples include:

```text
name
email
phone
address
date_of_birth
dob
gender
marital_status
nationality
religion
```

If these attributes are present, their values are replaced with:

```text
[MASKED]
```

Example:

```json
{
    "name": "[MASKED]",
    "email": "[MASKED]",
    "phone": "[MASKED]"
}
```

Professional information remains available for evaluation.

---

## Score Normalization

In addition to resume text normalization, the Fair Scoring Engine provides score normalization.

Scores are standardized into the configured ATS range:

```text
0 – 100
```

Min-max normalization is used to transform scores from a defined source range into the required output range.

Conceptually:

```text
Normalized Score =
(Score - Source Minimum)
------------------------
(Source Maximum - Source Minimum)
```

The resulting proportional value is then mapped to the configured output score range.

---

## Score Boundary Handling

Scores outside the expected source range are restricted to the defined boundaries.

For example, when the source range is:

```text
0 – 100
```

a value greater than 100 cannot produce a normalized ATS score greater than 100.

Similarly, values below 0 cannot produce a negative normalized score.

---

## Missing and Invalid Scores

The implementation also provides basic protection against missing or invalid score inputs.

Missing scores are handled safely rather than causing the entire candidate evaluation process to fail.

This improves the robustness of the scoring pipeline when candidate data is incomplete.

---

## Sample Normalization Result

Input:

```json
{
    "name": "Candidate A",
    "email": "candidate@example.com",
    "gender": "Female",
    "summary": "  DATA   SCIENTIST with experience in Machine Learning  ",
    "skills": [
        "PYTHON",
        " SQL ",
        "python"
    ]
}
```

Output:

```json
{
    "name": "[MASKED]",
    "email": "[MASKED]",
    "gender": "[MASKED]",
    "summary": "data scientist with experience in machine learning",
    "skills": [
        "python",
        "sql"
    ]
}
```

---

## Testing Result

The implemented normalizer was tested with:

- Inconsistent capitalization
- Repeated whitespace
- Duplicate skills
- Personal information
- Professional resume information

The test successfully generated:

```text
summary:
data scientist with experience in machine learning and analytics.

skills:
python
sql
machine learning

experience:
worked as a data analyst for two years.
```

Personal fields were successfully replaced with:

```text
[MASKED]
```

All normalization tests passed successfully as part of the Day 15 fairness engine test.

---

## Benefits

Resume normalization provides:

- Consistent candidate data.
- Cleaner text representation.
- Reduced duplicate information.
- Better input quality for downstream modules.
- Standardized score ranges.
- Safer handling of personal information.
- Improved consistency across candidate evaluations.

---

## Integration

The normalization layer can operate before downstream components such as:

```text
Resume Parsing
      ↓
Structured Candidate Data
      ↓
Resume Normalization
      ↓
Fairness Controls
      ↓
ATS Scoring
      ↓
Candidate Ranking
      ↓
Shortlisting
```

This enables standardized information to flow through the candidate evaluation pipeline.

---

## Conclusion

The Day 15 Normalization Logic provides a standardized preprocessing mechanism for candidate information and evaluation scores.

By cleaning text, standardizing capitalization, removing duplicates, masking configured personal information, and normalizing scores, the module improves the consistency and reliability of candidate evaluation while supporting the broader fairness objectives of the resume screening system.