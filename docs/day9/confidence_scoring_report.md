# Confidence Scoring Report

## Overview

The Skill Extraction Engine assigns confidence scores to indicate how accurately each skill was identified.

---

## Confidence Levels

| Match Type | Confidence |
|------------|------------|
| Exact Skill Match | 1.00 |
| Synonym Match | 0.95 |
| Spelling Variation | 0.90 |
| Stack Expansion | 0.85 |

---

## Purpose

Confidence scores help prioritize highly reliable skill matches while still recognizing equivalent skill names and technology stacks.

---

## Example

Resume:

```
Experienced in Python3, SQL Server and MERN Stack.
```

Output:

| Skill | Confidence |
|--------|------------|
| Python | 0.95 |
| SQL | 0.95 |
| MongoDB | 0.85 |
| Express.js | 0.85 |
| React | 0.85 |
| Node.js | 0.85 |

---

## Advantages

- Improves ATS accuracy
- Reduces false positives
- Standardizes extracted skills
- Supports candidate ranking
- Enables future machine learning enhancements