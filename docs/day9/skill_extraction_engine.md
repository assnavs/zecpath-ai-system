# Skill Extraction Engine

## Overview

The Skill Extraction Engine is responsible for identifying technical, business, and creative skills from resume text. It processes cleaned resume content, matches skills using a master skill dictionary, normalizes skill names, expands predefined technology stacks, removes duplicate entries, and generates structured JSON output with confidence scores.

---

## Objectives

- Extract skills from resume text
- Support technical, business, and creative skills
- Detect synonyms and spelling variations
- Expand technology stacks (MERN, MEAN)
- Normalize extracted skills
- Assign confidence scores
- Remove duplicate skills
- Produce structured JSON output

---

## Workflow

1. Load the master skill dictionary.
2. Read the resume text.
3. Match skills using dictionary entries.
4. Normalize skill names.
5. Expand technology stacks.
6. Remove duplicate skills.
7. Assign confidence scores.
8. Return structured JSON.

---

## Features

- Dictionary-based skill extraction
- Skill normalization
- Synonym handling
- Spelling variation detection
- Stack expansion
- Confidence scoring
- Duplicate removal
- Structured output generation

---

## Output Example

```json
{
    "total_skills": 11,
    "skills": [
        {
            "skill": "Python",
            "category": "Programming",
            "confidence": 1.0
        }
    ]
}
```