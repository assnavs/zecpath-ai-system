# Experience Parser

## Overview

The Experience Parser extracts employment history from cleaned resume text and converts it into a structured format for ATS processing.

## Objectives

- Extract company names
- Extract job titles
- Identify start and end dates
- Calculate employment duration
- Generate structured experience objects

## Workflow

1. Read cleaned resume text.
2. Detect employment date ranges.
3. Extract company and job title.
4. Calculate duration in months.
5. Build structured experience records.

## Features

- Company extraction
- Job title extraction
- Date parsing
- Duration calculation
- Total experience calculation
- Structured JSON output

## Sample Output

```json
{
    "company": "ABC Technologies",
    "job_title": "Data Analyst",
    "start_date": "Jan 2022",
    "end_date": "Dec 2023",
    "duration_months": 23
}
```