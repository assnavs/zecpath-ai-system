# AI Storage Structure Design

## Overview

This document defines how AI-related data is stored throughout the Zecpath AI Job Portal. The storage structure is designed to organize recruitment data in a standardized format, making it easier for different AI modules to access, process, and update information during the hiring lifecycle.

---

# 1. Resume Storage

Each uploaded resume is stored along with its metadata.

```json
{
    "candidate_id": "CAND001",
    "resume_file": "resume.pdf",
    "file_type": "PDF",
    "upload_timestamp": "2026-07-24T10:30:00Z",
    "status": "Uploaded"
}
```

---

# 2. Parsed Profile Storage

After resume parsing, the extracted candidate information is stored as a structured profile.

```json
{
    "candidate_id": "CAND001",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91XXXXXXXXXX",
    "skills": [
        "Python",
        "SQL",
        "Power BI"
    ],
    "education": "B.Tech Computer Science",
    "experience": "2 Years"
}
```

---

# 3. ATS Score Storage

The ATS Engine evaluates every candidate against a specific job description.

```json
{
    "candidate_id": "CAND001",
    "job_id": "JOB101",
    "ats_score": 87,
    "matching_skills": 15,
    "missing_skills": 2,
    "model_version": "ATS_v1.0"
}
```

---

# 4. Screening Report Storage

The AI Screening module stores screening results after evaluating the candidate profile.

```json
{
    "candidate_id": "CAND001",
    "screening_status": "Qualified",
    "strengths": [
        "Strong SQL",
        "Excellent Python"
    ],
    "weaknesses": [
        "Limited Cloud Experience"
    ]
}
```

---

# 5. Interview Result Storage

The Interview AI stores interview evaluation results.

```json
{
    "candidate_id": "CAND001",
    "interview_score": 90,
    "communication": "Excellent",
    "technical_score": 88,
    "recommendation": "Selected"
}
```

---

# Summary

The storage structures are standardized to ensure consistency across all AI modules. Every module stores its output in a structured format, enabling seamless integration with ATS, AI Screening, Interview Evaluation, and Recruitment Analytics systems.