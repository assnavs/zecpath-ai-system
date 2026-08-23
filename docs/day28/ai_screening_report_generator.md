# Day 28 – AI Screening Report Generator

## 1. Objective

The AI Screening Report Generator transforms outputs from the existing AI screening and evaluation components into a structured, recruiter-friendly screening report.

The generator combines candidate information, screening answers, evaluation results, strengths, risks, missing information, and shortlisting decisions into a single report.

## 2. Processing Capabilities

The Day 28 report generator supports:

- Structured screening report generation
- Key answer extraction
- Candidate information summarization
- Strength identification
- Risk identification
- Missing data detection
- Salary expectation highlighting
- Availability highlighting
- Skill confirmation highlighting
- ATS evaluation integration
- Screening evaluation integration
- Confidence and communication evaluation integration
- Shortlisting decision integration
- Recruiter-friendly recommendation generation
- JSON report export
- Plain-text report generation

## 3. Report Generation Flow

Candidate Screening Data
        |
        v
Evaluation Output Collection
        |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
ATS Evaluation       Screening Evaluation    Communication
                                             Signal Evaluation
        |                      |                      |
        +----------------------+----------------------+
                               |
                               v
                    Candidate Information
                               |
                               v
                     Key Answer Extraction
                               |
                               v
              +----------------+----------------+
              |                |                |
              v                v                v
          Strengths          Risks         Missing Data
              |                |                |
              +----------------+----------------+
                               |
                               v
                     Screening Highlights
                               |
                               v
                    Recruiter Recommendation
                               |
                               v
                    Structured Screening Report

## 4. Candidate Information

The report contains basic candidate information including:

- Candidate name
- Target job role

This provides recruiters with the primary context required when reviewing the screening report.

## 5. Key Answer Extraction

The generator extracts important candidate answers from the screening workflow.

Each extracted answer can contain:

- Question ID
- Question
- Candidate answer
- Detected answer intent

This allows recruiters to review the important responses without examining the complete screening interaction.

## 6. Strength Identification

The report generator identifies positive indicators from the available evaluation results.

Possible strengths include:

- Strong ATS evaluation score
- Good ATS evaluation score
- Strong observable communication signals
- Moderate observable communication signals
- Relevant skills confirmed during screening
- Candidate availability information provided

These strengths are based on available screening signals and evaluation outputs.

## 7. Risk Identification

The generator identifies observable screening risks from the available data.

Possible risks include:

- Low ATS evaluation score
- ATS evaluation requiring review
- Communication signals requiring improvement
- Hesitation indicators detected
- Uncertainty indicators detected

These are observable screening indicators and are not intended to represent psychological or personality assessments.

## 8. Missing Data Detection

The report identifies important information that has not been provided.

The generator checks for missing:

- Candidate name
- Job role
- Salary expectation
- Availability
- Skill confirmations

This helps recruiters identify information that may need additional clarification during the recruitment process.

## 9. Screening Highlights

The report provides a quick summary of important candidate information.

The highlights section can contain:

- Salary expectation
- Availability
- Confirmed skills

This allows recruiters to quickly review important screening information.

## 10. Evaluation Integration

The report generator organizes results from existing evaluation components.

### 10.1 ATS Evaluation

The report can include the existing ATS evaluation output, such as:

- Overall ATS score
- ATS recommendation
- Score breakdown

### 10.2 Screening Evaluation

The report can include the existing screening evaluation output, including:

- Final screening score
- Per-question evaluation information
- Screening explanation

### 10.3 Confidence and Communication Evaluation

The report can include the existing communication-signal evaluation, such as:

- Confidence score
- Communication strength
- Hesitation signals
- Response characteristics
- Sentiment
- Uncertainty
- Consistency

The confidence information represents observable communication signals and is not a psychological assessment.

## 11. Shortlisting Integration

The report can include the decision generated by the existing candidate shortlisting workflow.

The shortlisting information is preserved inside the final report so that recruiters can view the evaluation and decision together.

Possible decisions can include:

- Shortlisted
- Review
- Rejected

## 12. Recommendation Generation

The generator produces a recruiter-friendly recommendation.

When an existing shortlisting decision is available, that decision is used.

If a shortlisting decision is not available, the ATS score is used as a fallback.

The fallback rules are:

- 80 and above → Shortlisted
- 60 to 79 → Review
- Below 60 → Rejected

## 13. Structured Report Output

The generated report is organized into the following major sections:

- Report type
- Candidate information
- Summary
- Screening highlights
- Evaluation results
- Shortlisting information
- Final recommendation

The summary contains:

- Key answers
- Strengths
- Risks
- Missing data

This structure provides a consistent format for downstream recruitment workflows.

## 14. Export Formats

The report generator supports two export formats.

### 14.1 JSON Export

The structured screening report can be exported as JSON.

This format can be used by downstream applications and other components of the screening workflow.

### 14.2 Plain-Text Report

The generator can also create a readable plain-text version of the report.

The plain-text report includes:

- Candidate information
- Key answers
- Strengths
- Risks
- Missing data
- Salary expectation
- Availability
- Skills
- Final recommendation

## 15. Implementation

Main implementation:

screening_ai/report_generator.py

Automated tests:

tests/test_report_generator.py

## 16. Integration with Existing System

The AI Screening Report Generator acts as a reporting layer above the existing screening components.

It can consume outputs from:

- Answer Intent and Understanding Engine
- ATS Scoring Engine
- Screening Scoring Engine
- Confidence and Sentiment Analysis Engine
- Candidate Shortlisting workflow

The report generator does not replace these components.

Instead, it organizes their outputs into a single recruiter-friendly screening report.

## 17. Testing

The Day 28 automated test suite validates:

- Report generator creation
- Key answer extraction
- Strength detection
- Missing data detection
- Risk detection
- Shortlisting-based recommendation
- ATS-based fallback recommendation
- Complete report generation
- Required summary sections
- Plain-text report generation
- JSON export

## Test Result

All Day 28 AI Screening Report Generator tests passed successfully.

11 passed in 0.11s

## 18. Day 28 Deliverable

The completed AI Screening Report Generator provides a structured reporting layer for the AI screening workflow.

It combines multiple screening and evaluation outputs into a recruiter-friendly report containing:

- Candidate information
- Key screening answers
- Strengths
- Risks
- Missing information
- Screening highlights
- ATS evaluation
- Screening evaluation
- Communication evaluation
- Shortlisting information
- Final recommendation

The report can be exported as structured JSON or generated as readable plain text.

The implementation is supported by automated tests and integrates with the existing AI screening architecture without replacing the existing evaluation components.



