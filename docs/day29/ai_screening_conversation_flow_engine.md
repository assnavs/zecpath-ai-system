# Day 29 – AI Screening Conversation Flow Engine

## 1. Objective

The AI Screening Conversation Flow Engine controls the state-based flow of the candidate screening conversation.

The engine manages conversation states, response handling, retry behaviour, clarification, redirection, and continuation after maximum retries.

The purpose is to provide a structured conversation flow for the existing AI screening workflow.

## 2. Processing Capabilities

The Day 29 engine supports:

- Conversation state management
- State transition handling
- Candidate response evaluation
- Silence detection handling
- Missing or vague response handling
- Off-topic response handling
- Unknown response handling
- Interrupted response handling
- Retry management
- Question repetition
- Question clarification
- Maximum retry handling
- Continuation with available information
- Structured transition output

## 3. Conversation Flow

The configured conversation flow contains the following states:

Start
        |
        v
Asking
        |
        v
Listening
        |
        v
Evaluating
        |
        v
Decision
        |
        v
Completed

The flow represents the major stages of the AI screening interaction.

## 4. Conversation States

### 4.1 Start

The initial state before the screening question is presented.

Next state:

Asking

### 4.2 Asking

The AI asks the candidate the current screening question.

Next state:

Listening

### 4.3 Listening

The AI waits for and receives the candidate response.

Next state:

Evaluating

### 4.4 Evaluating

The candidate response is analyzed using available screening and communication signals.

The evaluation can consider:

- Answer intent
- Relevance
- Completeness
- Communication signals

Next state:

Decision

### 4.5 Decision

The conversation engine decides how to handle the candidate response.

Possible actions include:

- Continue
- Retry
- Clarify
- Redirect

### 4.6 Completed

The screening conversation has completed successfully.

There is no next state after completion.

## 5. Response Handling

The engine supports several configured response types.

### 5.1 Silence

When no candidate response is received, the engine can retry the question.

Configured action:

Retry

### 5.2 Missing or Vague Response

When the candidate response does not provide enough information, the engine requests additional detail.

Configured action:

Clarify

### 5.3 Off-Topic Response

When the response is not related to the current screening question, the engine redirects the candidate back to the question.

Configured action:

Redirect

### 5.4 Unknown Response

When the response type cannot be identified, the engine uses the configured clarification behaviour.

Configured action:

Clarify

### 5.5 Understood Response

When the candidate response is understood, the conversation can continue to the next configured state.

Configured action:

Continue

### 5.6 Interrupted Response

When the response appears to have been interrupted, the engine requests the candidate to continue.

Configured action:

Retry

## 6. Retry Policy

The conversation flow uses a configurable retry policy.

Maximum retries:

2

The configured retry actions are:

1. Repeat question
2. Clarify question

After the maximum number of retries is reached, the engine uses:

Continue with available information

This allows the screening workflow to continue without repeatedly asking the same question.

## 7. Transition Handling

The engine provides a structured transition method.

Each transition can contain:

- Current state
- Next state
- Response type
- Action
- Message
- Retry count
- Continuation status

This provides a consistent interface for downstream conversation components.

## 8. Configuration

The conversation flow is configuration-driven.

Configuration file:

data/conversation_flow_configuration.json

The configuration defines:

- Conversation states
- State transitions
- Response rules
- Response messages
- Retry policy
- Maximum retry count
- Retry actions
- Post-retry behaviour

## 9. Implementation

Main implementation:

screening_ai/conversation_flow_engine.py

Configuration:

data/conversation_flow_configuration.json

Automated tests:

tests/test_conversation_flow_engine.py

## 10. Integration

The Conversation Flow Engine provides a control layer for the AI screening interaction.

It can work with existing screening components such as:

- Answer Intent and Understanding Engine
- Screening workflow
- Transcript processing
- Communication signal analysis
- Screening scoring
- AI screening report generation

The engine controls the conversation flow rather than replacing the existing evaluation components.

## 11. Testing

The Day 29 automated test suite validates:

- Configuration file availability
- Initial state
- State transitions
- Unknown state handling
- Understood response handling
- Silence response handling
- Vague response handling
- Off-topic response handling
- Unknown response handling
- Retry policy
- Second retry behaviour
- Maximum retry behaviour
- Successful transitions
- Silence transitions
- Maximum retry transitions
- Clarification transitions
- Interrupted response handling
- Complete flow output
- Completed state handling

## Test Result

All Day 29 Conversation Flow Engine tests passed successfully.

19 passed in 0.11s

## 12. Day 29 Deliverable

The completed AI Screening Conversation Flow Engine provides a configurable state-based conversation layer for the screening workflow.

It manages:

- Conversation states
- Response handling
- Retry behaviour
- Clarification
- Redirection
- Interrupted responses
- Maximum retry handling
- Structured conversation transitions

The implementation is configuration-driven and supported by automated tests.

The Day 29 test suite completed successfully with 19 passing tests.
