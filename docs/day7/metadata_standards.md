# AI Metadata Standards

## Overview

This document defines the metadata standards used across the AI Recruitment and Job Portal System. Metadata provides additional information about stored records, enabling data tracking, version control, auditing, and seamless communication between different AI modules.

By following common metadata standards, every module in the system can identify, process, and update recruitment data consistently throughout the hiring lifecycle.

---

# Standard Metadata Fields

The following metadata fields are maintained for every AI-generated record.

| Field | Description |
|--------|-------------|
| Candidate ID | Unique identifier assigned to each candidate |
| Job ID | Unique identifier assigned to each job posting |
| Record ID | Unique identifier for each stored record |
| Model Version | AI model version used during processing |
| Timestamp | Date and time when the record was generated or updated |
| Processing Status | Current processing stage of the record |
| Source Module | AI module that generated the record |
| Data Version | Version number of the stored data |

---

# Metadata Definitions

## Candidate ID

Every candidate is assigned a unique identifier that remains constant throughout the recruitment process.

Example:

```text
CAND001
```

---

## Job ID

Every job posting receives a unique identifier to associate candidates with specific recruitment opportunities.

Example:

```text
JOB101
```

---

## Record ID

Each stored object has its own unique identifier to distinguish individual records.

Example:

```text
REC000125
```

---

## Model Version

The AI model version identifies which version of the recruitment model processed the data.

Example:

```text
ATS_v1.0
```

---

## Timestamp

Every record stores the creation or update time to support auditing and historical tracking.

Example:

```text
2026-07-24T10:30:00Z
```

---

## Processing Status

This field indicates the current stage of the recruitment process.

Possible values include:

- Uploaded
- Parsed
- ATS Scored
- Screened
- Interview Completed
- Selected
- Rejected

---

## Source Module

This identifies the AI component responsible for generating the record.

Examples include:

- Resume Parser
- ATS Engine
- Screening AI
- Interview AI
- Recruitment Dashboard

---

## Data Version

Whenever stored information is modified, the data version is updated to maintain version history.

Example:

```text
Version 1
Version 2
Version 3
```

---

# Metadata Example

```json
{
    "candidate_id": "CAND001",
    "job_id": "JOB101",
    "record_id": "REC000125",
    "model_version": "ATS_v1.0",
    "timestamp": "2026-07-24T10:30:00Z",
    "processing_status": "ATS Scored",
    "source_module": "ATS Engine",
    "data_version": "Version 1"
}
```

---

# Benefits of Metadata Standards

Implementing metadata standards provides several advantages:

- Ensures consistent identification of records.
- Simplifies communication between AI modules.
- Supports version control and audit trails.
- Improves traceability throughout the recruitment process.
- Enables easier debugging and monitoring.
- Facilitates future AI model improvements.
- Supports large-scale recruitment analytics.
- Enhances overall data governance.

---

# Conclusion

The metadata standards establish a common framework for identifying, tracking, and managing recruitment data across the AI Recruitment and Job Portal System. Standardized metadata improves consistency, interoperability, and maintainability while supporting future enhancements such as AI model versioning, analytics, and intelligent recruitment workflows.