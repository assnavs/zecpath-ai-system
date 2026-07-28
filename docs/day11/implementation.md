# Day 11 – Education & Certification Parsing

## Objective

Develop modules to extract education and certification details from resumes, normalize academic qualifications, and evaluate education relevance for the ATS system.

## Modules Implemented

- Education Parser
- Education Normalizer
- Certification Parser
- Education Relevance Scorer

## Files Created

### Data

- education_dictionary.json
- certification_dictionary.json
- education_relevance.json

### Parsers

- education_normalizer.py
- education_parser.py
- certification_parser.py

### Scoring

- education_relevance_scorer.py

### Tests

- test_education_parser.py
- test_certification_parser.py

## Features

### Education Parser

- Extracts degree
- Extracts institution
- Extracts graduation year
- Normalizes degree names

### Certification Parser

- Detects certifications
- Identifies issuer
- Categorizes certifications
- Extracts certification year

### Education Relevance Scorer

- Maps degrees into academic domains
- Produces structured relevance output

## Technologies Used

- Python
- JSON
- Regular Expressions
- Rule-Based Parsing

## Outcome

Successfully implemented education and certification extraction modules with structured outputs and relevance scoring compatible with the existing ATS architecture.