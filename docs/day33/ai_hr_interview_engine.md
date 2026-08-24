# Day 33 – AI HR Interview Engine

## 1. Objective

Day 33 focuses on establishing the foundational AI HR Interview Engine for the Zecpath AI system.

The implementation builds on the existing HR screening dataset and existing project architecture.

The objective is to support:

- HR interview categories
- Role-based question generation
- Fresher and experienced candidates
- Technical and non-technical role classification
- Interview state management
- Candidate response capture
- Follow-up eligibility
- Conversation phases
- Interview completion handling

No new project architecture or folder structure was introduced.

## 2. Existing HR Screening Dataset

The existing HR screening dataset is located at:

data/hr_screening_dataset.json

The dataset contains role-based HR screening questions.

Existing roles include:

- Data Scientist
- Data Analyst
- Software Engineer
- HR Coordinator

Each role contains seven question categories:

- Introduction
- Education
- Experience
- Skills
- Location
- Salary
- Notice Period

Each question contains structured information including:

- Question ID
- Category
- Question
- Expected answer type
- Mandatory status
- Scoring importance

## 3. Interview Engine

The Interview Engine is implemented in:

interview_ai/interview.py

The main class is:

InterviewAI

The engine loads the existing HR screening dataset and uses it to generate interview questions.

## 4. HR Interview Categories

The Interview Engine defines the following HR interview categories:

- Self-introduction
- Career journey
- Strengths & weaknesses
- Teamwork & culture fit
- Career goals
- Availability & commitment

These categories represent the foundational HR interview areas supported by the engine.

## 5. Conversation Phases

The interview follows four defined conversation phases:

1. Introduction
2. Core HR Questions
3. Role-Based Evaluation
4. Closing

The engine maintains the current phase as part of the interview state.

## 6. Technical and Non-Technical Role Detection

The Interview Engine classifies roles as either technical or non-technical.

Technical roles currently include roles such as:

- Data Scientist
- Data Analyst
- Software Engineer
- ML Engineer
- AI Engineer
- Backend Developer
- Frontend Developer
- Full Stack Developer

Roles outside the configured technical-role list are classified as non-technical.

For example:

HR Coordinator

is classified as:

non_technical

## 7. Experience Level Handling

The Interview Engine supports two experience levels:

- Fresher
- Experienced

The selected experience level is included in the generated question metadata.

Unsupported experience levels are rejected using validation.

## 8. Role-Based Question Generation

The engine generates questions using the existing HR screening dataset.

Each generated question is enriched with:

- Role
- Role type
- Experience level

For example, a Data Scientist interview question is identified as:

Role:
Data Scientist

Role type:
technical

Experience level:
fresher or experienced

The existing dataset remains the source for the actual interview questions.

## 9. Interview State Management

The Interview Engine maintains an interview state containing:

- Role
- Experience level
- Current phase
- Question ID
- Candidate response
- Response received status
- Follow-up eligibility
- Completion status

The initial interview state begins in the introduction phase and is marked as incomplete.

## 10. Interview Start

The start_interview() operation begins the interview in the introduction phase.

The first available Introduction question is selected from the existing role-based dataset.

The selected question ID is stored in the interview state.

## 11. Candidate Response Capture

The capture_response() operation accepts the candidate's response.

The response is cleaned using basic whitespace normalization and stored in the interview state.

The engine records whether a response was received.

## 12. Follow-Up Eligibility

The engine determines whether a follow-up question may be appropriate based on response length.

Short responses containing fewer than five words are marked as eligible for follow-up.

More detailed responses are not marked for follow-up.

## 13. Phase Transition

The move_to_phase() operation allows the interview to transition between valid conversation phases.

When moving to a new phase:

- The current phase is updated.
- The question ID is reset.
- A suitable question is selected when available.
- The interview state is updated.

The role-based evaluation phase selects the Skills question.

## 14. Closing Phase

When the interview moves to the closing phase, the interview is marked as completed.

The returned result exposes the completion state directly.

This ensures that the interview completion status can be consumed by the calling system.

## 15. Day 33 Issues Identified and Resolved

Two implementation issues were identified during Day 33 testing.

### 15.1 Non-Technical Role Validation

The test attempted to initialize:

HR Coordinator

The role was initially rejected because it was not present in the HR screening dataset.

The role was added to the existing dataset using the same seven-question structure as the other supported roles.

The role can now be classified correctly as non-technical.

### 15.2 Closing Completion State

The closing phase correctly updated the internal interview state to completed.

However, the completion value was initially available only inside the nested state object.

The return structure was updated so that the completion value is also directly accessible from the result.

## 16. Regression Testing

The Day 33 Interview Engine test suite was executed using:

python -m pytest tests/test_day33_interview_engine.py -q

Final result:

13 passed in 0.13s

All Day 33 Interview Engine tests passed successfully.

## 17. HR Dataset Regression

The existing HR screening dataset regression test was also executed.

Command:

python -m pytest tests/test_hr_screening_dataset.py -q

Result:

6 passed in 0.05s

The existing HR dataset functionality remained stable after the Day 33 changes.

## 18. Day 33 Validation Summary

| Evaluation | Result |
|---|---|
| HR dataset regression | 6 passed |
| Interview Engine tests | 13 passed |
| Interview initialization | Passed |
| HR categories | Passed |
| Conversation phases | Passed |
| Technical role detection | Passed |
| Non-technical role detection | Passed |
| Role-based question generation | Passed |
| Response capture | Passed |
| Follow-up eligibility | Passed |
| Phase transition | Passed |
| Closing completion | Passed |

## 19. Day 33 Deliverable

Day 33 establishes a foundational AI HR Interview Engine using the existing Zecpath AI architecture.

The implementation provides structured interview state management, role-based question generation, technical/non-technical role classification, experience-level handling, response capture, follow-up eligibility, conversation phase management, and interview completion handling.

The final regression tests confirm that the Day 33 Interview Engine and existing HR screening dataset are functioning successfully.

No unnecessary architectural replacement was performed.
