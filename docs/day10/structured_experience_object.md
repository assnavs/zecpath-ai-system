# Structured Experience Object

## Purpose

The Experience Parser converts unstructured employment history into structured JSON objects for downstream ATS modules.

## Structure

Each experience contains:

- Company
- Job Title
- Start Date
- End Date
- Duration (Months)

Example:

```json
{
    "company": "XYZ Solutions",
    "job_title": "Business Analyst",
    "start_date": "Jan 2024",
    "end_date": "Present",
    "duration_months": 30
}
```

## Overall Output

```json
{
    "total_experience_months": 53,
    "experience_count": 2,
    "experiences": []
}
```

## Advantages

- Standardized experience records
- Easy ATS integration
- Supports relevance scoring
- Improves candidate analysis