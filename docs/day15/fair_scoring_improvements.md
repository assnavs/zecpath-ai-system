# Fair Scoring Improvements

## Overview

The Fair Scoring Improvements module was developed to improve the consistency and fairness of candidate evaluation within the Zecpath AI resume screening system.

Traditional resume screening systems can become overly dependent on exact keyword matches or inconsistent score ranges. Candidate resumes may also contain personal information that is not necessary for determining professional suitability.

The Day 15 implementation introduces fairness-oriented controls that standardize candidate evaluation, limit excessive keyword influence, normalize evaluation scores, and prevent selected non-essential personal attributes from being used during screening.

---

## Objective

The primary objective of the Fair Scoring Improvements module is to provide a more standardized and transparent candidate evaluation process.

The implementation focuses on:

- Standardizing evaluation scores.
- Reducing excessive dependence on keyword matching.
- Supporting semantic and contextual evaluation signals.
- Masking selected non-essential personal information.
- Generating transparent fairness indicators.
- Identifying configurations that may require further review.

---

## Fairness-Oriented Evaluation

Candidate evaluation should focus primarily on job-relevant information such as:

- Skills
- Experience
- Education
- Semantic relevance
- Professional qualifications

Personal attributes that are not necessary for the screening decision should not influence candidate scoring.

The implemented fairness layer therefore separates relevant professional information from selected personal information before candidate evaluation.

---

## Score Normalization

Candidate evaluation components may generate scores that need to be represented consistently.

The Fair Scoring Engine provides score normalization so evaluation values can be standardized to the configured range.

The current standardized range is:

```text
0 – 100
```

The normalization process ensures that scores remain within the expected evaluation boundaries.

For example:

```text
Experience Relevance = 82
Education Alignment = 78
Semantic Similarity = 88
```

remain represented consistently within the 0–100 scoring range.

---

## Reducing Keyword Dependence

Keyword matching is useful for identifying required technical skills, but candidate evaluation should not depend excessively on keyword occurrence alone.

A resume may contain repeated keywords without demonstrating sufficient contextual relevance or practical experience.

The implementation therefore introduces a configurable keyword score cap.

Current configuration:

```text
Keyword Score Cap = 85
```

During testing, the original keyword score was:

```text
96
```

After applying the fairness control:

```text
96 → 85
```

This prevents an unusually high keyword-based score from dominating the evaluation.

---

## Balanced Evaluation Signals

The fairness-oriented scoring approach supports multiple candidate evaluation signals, including:

```text
Keyword / Skill Match
        +
Experience Relevance
        +
Education Alignment
        +
Semantic Similarity
```

Using multiple evaluation dimensions provides a broader representation of candidate suitability than relying only on exact keyword matching.

---

## Personal Attribute Masking

Selected non-essential personal attributes are masked before candidate evaluation.

Examples include:

- Name
- Email
- Phone number
- Address
- Date of birth
- Gender
- Marital status
- Nationality
- Religion

When these fields are present in the structured resume data, their values are replaced with:

```text
[MASKED]
```

For example:

```text
Name: [MASKED]
Email: [MASKED]
Phone: [MASKED]
```

The masking mechanism is intended to prevent these fields from becoming scoring inputs.

---

## Configurable Fairness Controls

Fairness-related settings are maintained in:

```text
data/fairness_configuration.json
```

This configuration controls:

- Minimum score
- Maximum score
- Keyword score cap
- Personal attributes to mask
- Keyword dependency threshold
- Semantic contribution threshold

Separating these settings from application logic makes the fairness controls easier to maintain and adjust.

---

## Bias Indicators

The Fair Scoring Engine generates rule-based indicators that help identify configurations that may require review.

The indicators include:

- Whether personal attributes were masked.
- Whether keyword dependency remains within the configured threshold.
- Whether semantic contribution meets the configured threshold.
- Whether any fairness-related review flags were generated.

Example:

```json
{
    "personal_attributes_masked": true,
    "keyword_dependency_reduced": true,
    "semantic_contribution_sufficient": true,
    "bias_flags": [],
    "requires_review": false
}
```

These indicators provide transparency into the implemented fairness controls.

They should not be interpreted as proof that an evaluation system is completely free from bias.

---

## Testing and Validation

The Fair Scoring Engine was tested using structured candidate information containing both professional information and selected personal attributes.

The test confirmed:

```text
Personal attributes → Masked
Resume text → Normalized
Duplicate skills → Removed
Keyword score → Limited from 96 to 85
Experience score → 82
Education score → 78
Semantic score → 88
Bias flags → None for tested configuration
```

The automated test completed successfully.

---

## Benefits

The implemented improvements provide:

- More consistent candidate evaluation.
- Reduced excessive keyword influence.
- Standardized scoring.
- Separation of selected personal information from evaluation inputs.
- Transparent fairness indicators.
- Configurable fairness controls.
- Better support for explainable candidate screening.

---

## Limitations

The implemented fairness controls reduce specific identifiable sources of unwanted influence but do not guarantee that the complete recruitment system is bias-free.

Fairness can also depend on factors such as:

- Training data
- Job descriptions
- Historical recruitment decisions
- Scoring configurations
- Model behavior
- Organizational policies

Therefore, fairness should continue to be evaluated throughout future system development.

---

## Conclusion

The Fair Scoring Improvements introduced on Day 15 strengthen the candidate evaluation pipeline by combining score normalization, keyword dependency control, personal attribute masking, and transparent fairness indicators.

These improvements create a more standardized and explainable evaluation process while providing a foundation for future fairness analysis and monitoring.