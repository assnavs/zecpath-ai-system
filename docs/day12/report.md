# Day 12 Report

## Task

Semantic Matching Engine

---

## Objective

Develop a semantic matching engine capable of comparing resumes and job descriptions using sentence embeddings and cosine similarity.

---

## Work Completed

- Created semantic similarity threshold configuration
- Implemented Semantic Matching Engine
- Integrated Sentence Transformer model
- Generated semantic embeddings
- Implemented cosine similarity calculation
- Developed section-wise similarity comparison
- Calculated overall similarity score
- Implemented match classification
- Performed unit testing

---

## Challenges

- Installed additional dependencies required for semantic embeddings.
- Resolved JSON serialization issue caused by NumPy float32 values by converting them to native Python float.
- Downloaded and initialized the pretrained Sentence Transformer model.

---

## Solution

Used the SentenceTransformer "all-MiniLM-L6-v2" model to generate contextual embeddings. Cosine similarity was used to compare resume and job description content. Threshold classification was implemented through a configurable JSON file.

---

## Testing

The Semantic Matching Engine was tested using sample resume and job description data.

The following components were verified:

- Embedding Generation
- Semantic Similarity Calculation
- Threshold Classification

All unit tests passed successfully.

---

## Outcome

Successfully implemented and tested the Semantic Matching Engine. The module accurately computes semantic similarity between resumes and job descriptions and produces structured similarity scores suitable for ATS candidate evaluation.