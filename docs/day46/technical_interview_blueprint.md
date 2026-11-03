# Day 46 — Technical Interview System Blueprint

## 1. Objective

The objective of Day 46 is to design and implement a role-based technical interview system that selects technical questions according to the candidate's job role and professional experience.

## 2. System Overview

The Technical Interview Engine is implemented as a separate module without modifying the existing HR Interview Engine.

Main components:

- Role-based technical question selection.
- Experience-level classification.
- Technical skill mapping.
- Interview section definition.
- Question response capture.
- Interview state transitions.

## 3. Supported Technical Roles

The initial configuration supports three technical roles.

| Role | Mapped Skills |
|---|---|
| MERN Developer | MongoDB, Express.js, React, Node.js, JavaScript |
| Java Developer | Java, OOP, Spring Boot, SQL, REST APIs |
| DevOps Engineer | Linux, Docker, Kubernetes, CI/CD, AWS, Monitoring |

These mappings are initial configurable examples.

## 4. Experience Classification

| Experience | Classification |
|---|---|
| 0–2 years | Entry |
| 3–4.99 years | Intermediate |
| 5 years and above | Advanced |

The classification is determined using the candidate's experience in years.

## 5. Interview Sections

The interview structure contains:

1. Introduction
2. Experience-based questions
3. Conceptual questions
4. Scenario-based questions

The configuration also defines evaluation and closing states.

## 6. Technical Implementation

The implementation consists of:

- `interview_ai/technical_interview_engine.py`
- `data/technical_interview_configuration.json`

The engine loads role-specific questions and skills from the configuration file.

## 7. Expected Output

The engine provides:

- Candidate role.
- Experience years.
- Experience classification.
- Initial interview state.
- Selected question.
- Total question count.
- Captured candidate responses.
- Structured evaluation input.

## 8. Scope and Limitations

The current implementation selects a question set based on the candidate's experience classification.

Adaptive difficulty changes based on candidate answers are not yet implemented.

The configured questions are initial demonstration examples and require further expansion and validation before production use.
