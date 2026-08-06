# ATS Architecture Diagrams

## Day 19 – ATS Documentation & Knowledge Transfer

## 1. Purpose

This document provides high-level technical architecture diagrams for the ATS implementation.

The diagrams describe the ATS processing components and their relationships for development and knowledge-transfer purposes.

They intentionally focus on the implemented ATS workflow and do not represent confidential organizational infrastructure or undisclosed product architecture.

---

# 2. High-Level ATS Architecture

```text
                    ┌─────────────────────┐
                    │    Resume Input     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Resume Parsers    │
                    │   PDF / DOCX Text   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Text Cleaner     │
                    │ Noise Normalization │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Resume Normalizer   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Section Classifier  │
                    │ Profile / Skills /  │
                    │ Experience / etc.   │
                    └──────────┬──────────┘
                               │
                               ▼
               ┌───────────────────────────────┐
               │ Structured Resume Processing │
               └───────────────┬───────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌────────────────┐
      │ Skill Match  │ │ Experience   │ │ Semantic Match │
      │ Processing   │ │ Relevance    │ │    Engine      │
      └──────┬───────┘ └──────┬───────┘ └───────┬────────┘
             │                │                 │
             └────────────────┼─────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ ATS Scoring Engine  │
                    │ Role-Based Weights  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Fairness Controls   │
                    │ & Normalization     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Candidate Ranking   │
                    │ & Shortlisting      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     ATS API         │
                    │ Structured Output   │
                    └─────────────────────┘
```

---

# 3. Resume Processing Architecture

```text
Resume File
    │
    ├──────────────┐
    │              │
    ▼              ▼
 PDF Reader     DOCX Reader
    │              │
    └──────┬───────┘
           │
           ▼
      Raw Resume Text
           │
           ▼
      Text Cleaner
           │
           ▼
    Normalized Text
           │
           ▼
  Section Classification
           │
           ├── PROFILE
           ├── SKILLS
           ├── WORK EXPERIENCE
           ├── EDUCATION
           ├── CERTIFICATIONS
           └── PROJECTS
           │
           ▼
 Structured Resume Information
```

---

# 4. Resume Header Processing

```text
Resume Start
    │
    ▼
Candidate Name
Current Designation
Contact Header
    │
    ▼
PROFILE
    │
    ▼
First Recognized Heading
    │
    ▼
Corresponding Resume Section
```

This design prevents resume header information from being unnecessarily classified as UNKNOWN.

---

# 5. Semantic Matching Architecture

```text
          Resume                         Job Description
             │                                  │
     ┌───────┼────────┐                ┌────────┼────────┐
     │       │        │                │        │        │
     ▼       ▼        ▼                ▼        ▼        ▼
   Skills Experience Projects        Skills Experience Projects
     │       │        │                │        │        │
     └───────┴────────┴────────────────┴────────┴────────┘
                              │
                              ▼
                  ┌──────────────────────┐
                  │ Batch Text Encoding  │
                  │ SentenceTransformer  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Normalized Embedding │
                  │      Vectors         │
                  └──────────┬───────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
       Skill Similarity  Experience       Project
                          Similarity       Similarity
            │                │                │
            └────────────────┼────────────────┘
                             │
                             ▼
                  Overall Semantic Score
                             │
                             ▼
                     Match Classification
```

---

# 6. Semantic Model Reuse

```text
SemanticMatchingEngine Instance 1
               │
               ▼
       Is Model Loaded?
               │
              NO
               │
               ▼
     Load all-MiniLM-L6-v2
               │
               ▼
        Store Shared Model
               │
               ▼
          Use Model


SemanticMatchingEngine Instance 2
               │
               ▼
       Is Model Loaded?
               │
              YES
               │
               ▼
       Reuse Shared Model
```

This avoids unnecessary repeated model initialization within the same running process.

---

# 7. ATS Scoring Architecture

```text
Skill Match
    │
    ├── × Role Skill Weight
    │
Experience Relevance
    │
    ├── × Role Experience Weight
    │
Education Alignment
    │
    ├── × Role Education Weight
    │
Semantic Similarity
    │
    └── × Role Semantic Weight
            │
            ▼
     Weighted Components
            │
            ▼
       Sum Components
            │
            ▼
      Overall ATS Score
            │
            ▼
       Recommendation
```

---

# 8. Scoring Formula

```text
Overall ATS Score

        =

(Skill Match × Skill Weight)

        +

(Experience Relevance × Experience Weight)

        +

(Education Alignment × Education Weight)

        +

(Semantic Similarity × Semantic Weight)
```

Weights are selected according to the configured target job role.

---

# 9. Role Configuration Flow

```text
Target Job Role
      │
      ▼
ATS Weight Configuration
      │
      ├── Skill Weight
      ├── Experience Weight
      ├── Education Weight
      └── Semantic Weight
      │
      ▼
Candidate Score Components
      │
      ▼
Weighted ATS Calculation
      │
      ▼
Overall Score
```

---

# 10. Candidate Ranking & Shortlisting Architecture

```text
Candidate Scores
      │
      ▼
Sort by Score
Highest → Lowest
      │
      ▼
Assign Rank
      │
      ▼
Apply Thresholds
      │
      ├───────────────┐
      │               │
      ▼               ▼
Shortlist          Review
Threshold          Threshold
      │               │
      └───────┬───────┘
              │
              ▼
      Candidate Decision
              │
       ┌──────┼──────┐
       ▼      ▼      ▼
 Shortlisted Review Rejected
              │
              ▼
       Top Candidate List
```

---

# 11. Fairness Processing Architecture

```text
Structured Resume
       │
       ▼
Resume Normalization
       │
       ▼
Personal Attribute Masking
       │
       ▼
Normalized Candidate Data
       │
       ▼
Scoring Controls
       │
       ├── Keyword Dependency Control
       ├── Semantic Contribution Check
       └── Score Normalization
       │
       ▼
Bias Indicator Evaluation
       │
       ├── No Flags
       │
       └── Review Required
       │
       ▼
Fairness Evaluation Result
```

---

# 12. ATS API Integration Architecture

```text
          Backend / Client
                 │
                 ▼
          ┌─────────────┐
          │   ATS API   │
          └──────┬──────┘
                 │
       ┌─────────┼─────────┐
       │         │         │
       ▼         ▼         ▼
    Parsing    Scoring  Shortlisting
       │         │         │
       └─────────┼─────────┘
                 │
                 ▼
        Existing ATS Modules
                 │
                 ▼
        Structured Response
                 │
                 ▼
          Backend / Client
```

---

# 13. API Processing Flow

```text
Request
   │
   ▼
Input Validation
   │
   ├── Invalid
   │      │
   │      ▼
   │ Structured Error Response
   │
   └── Valid
          │
          ▼
      ATS Processing
          │
          ▼
      Result Generation
          │
          ▼
   Structured API Response
```

---

# 14. ATS Testing Architecture

```text
Controlled Candidate Cases
           │
           ▼
      ATS Evaluation
           │
           ▼
     ATS Decision
           │
           ├──────────────┐
           │              │
           ▼              ▼
     Manual Decision   Comparison
                          │
                          ▼
                 Confusion Matrix
                          │
               ┌──────────┼──────────┐
               ▼          ▼          ▼
           Accuracy   Precision    Recall
                          │
                          ▼
                      F1 Score
                          │
                          ▼
                   Mismatch Cases
                          │
                          ▼
                 Improvement Backlog
```

---

# 15. Maintainability View

```text
                 ATS System
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
    Parsers       Scoring        API Layer
       │             │             │
       ▼             ▼             ▼
Normalization   Configuration   Contracts
       │             │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                   Tests
                     │
                     ▼
               Documentation
```

The modular organization allows individual components to be modified and tested without intentionally redesigning unrelated system areas.

---

# 16. Architecture Extension Points

Future development can extend the architecture through:

```text
Additional Resume Formats
          │
Additional Section Types
          │
Improved Entity Extraction
          │
Additional Job Roles
          │
Role-Specific Thresholds
          │
Expanded Fairness Testing
          │
Larger Validation Dataset
          │
Additional API Capabilities
          │
Production Monitoring
```

---

# 17. Conclusion

The ATS architecture separates resume processing, semantic analysis, scoring, fairness controls, candidate ranking, shortlisting, API integration, and testing into logical components.

The architecture is designed to remain explainable and configurable while allowing future developers to extend individual processing stages without requiring a complete system rewrite.