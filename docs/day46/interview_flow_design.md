# Day 46 — Technical Interview Flow Design

## 1. Objective

The objective is to define the flow and state transitions of a role-based technical interview session.

## 2. Interview Flow

The configured interview flow follows these states:

1. Introduction
2. Experience-based
3. Conceptual
4. Scenario-based
5. Evaluation
6. Closing
7. Completed

## 3. State Transition Model

| Current State | Next State |
|---|---|
| Introduction | Experience-based |
| Experience-based | Conceptual |
| Conceptual | Scenario-based |
| Scenario-based | Evaluation |
| Evaluation | Closing |
| Closing | Completed |

## 4. Interview Session Initialization

When a session starts, the engine:

- Validates the selected role.
- Validates the candidate's experience.
- Determines the experience category.
- Loads the configured question set.
- Initializes the interview state.
- Returns the first available question.

## 5. Response Capture

The `submit_response()` method:

1. Validates the answer type.
2. Retrieves the current question.
3. Stores the question, skill, difficulty, and candidate response.
4. Advances the question index.
5. Returns the next available question.

## 6. Evaluation Input

The `generate_evaluation_input()` method produces structured data containing:

- Candidate role.
- Experience classification.
- Submitted questions.
- Relevant technical skills.
- Question difficulty.
- Candidate answers.

This output can be used by a future technical scoring component.

## 7. State Management

The `advance_flow()` method uses the configured transitions to move between interview states.

The engine prevents transition to evaluation from the scenario-based state until all configured questions have received responses.

## 8. Testing and Validation

The Day 46 test suite validates:

- Experience classification.
- Role-to-skill mapping.
- Interview section structure.
- Interview initialization.
- Question selection.
- Response capture.
- Evaluation input generation.
- State transitions.
- Invalid role and experience inputs.
- Session reset behavior.

## 9. Limitations

The current implementation provides a configurable state flow and question response capture.

It does not yet provide automatic answer scoring, adaptive follow-up generation, or dynamic question difficulty changes.

These functions can be integrated in subsequent development tasks.
