# Day 24 - Speech-to-Text Processing and Transcript Cleaning

## 1. Objective

The Speech-to-Text Processing module processes transcript text generated from speech input and prepares it for downstream AI screening.

The processor cleans conversational speech, normalizes formatting, preserves important technical terminology, and produces consistent transcript output.

## 2. Processing Capabilities

The Day 24 processor supports:

- Filler-word removal
- Whitespace cleanup
- Case normalization
- Technical-term preservation
- Punctuation correction
- Interrupted speech handling
- Partial-answer handling
- Silence detection
- Mock speech-to-text processing
- Transcript cleaning integration

## 3. Transcript Cleaning Flow

Speech-to-Text Output
|
v
Filler Word Removal
|
v
Whitespace Cleanup
|
v
Case Normalization
|
v
Punctuation Correction
|
v
Clean Transcript

## 4. Filler Word Removal

The processor removes common conversational filler words such as:

- Um
- Uh
- Er
- Ah
- Hmm
- Like
- Actually
- Basically
- You know
- Sort of
- Kind of

Filler removal also handles nearby punctuation and preserves correct spacing.

## 5. Whitespace Cleanup

The processor normalizes multiple spaces into single spaces.

Example:

I   have    experience   in   SQL

becomes:

I have experience in SQL.

## 6. Case Normalization

The processor normalizes transcript capitalization while preserving technical terminology.

Examples of preserved technical terms include:

- Python
- SQL
- Java
- JavaScript
- TypeScript
- HTML
- CSS
- API
- AI
- ML
- NLP
- AWS
- Azure
- Power BI
- Excel
- MySQL
- PostgreSQL
- MongoDB
- Docker
- Kubernetes
- Git
- GitHub

## 7. Punctuation Correction

The processor ensures that cleaned transcript responses have consistent sentence-ending punctuation.

## 8. Interrupted and Partial Speech

The processor supports:

- Interrupted speech
- Partial answers
- Incomplete conversational responses

## 9. Silence Detection

The processing layer includes silence detection support for speech-to-text interaction handling.

## 10. Integration

The Speech-to-Text integration layer combines transcript processing with the cleaning pipeline.

The integration returns:

- Processing status
- Confidence score
- Cleaned transcript text

The current mock integration uses a confidence value of 0.95 for successful transcription.

## 11. Implementation

Main implementation:

utils/speech_to_text_processor.py

Automated tests:

tests/test_speech_to_text_processor.py

## 12. Testing

The Day 24 automated test suite validates:

- STT test-case existence
- Filler-word removal
- Whitespace cleanup
- Case normalization
- Punctuation correction
- Interrupted speech handling
- Partial-answer handling
- Silence detection
- Mock STT service
- STT integration pipeline
- Multiple STT test cases

## Test Result

All Day 24 Speech-to-Text Processing tests passed successfully.

11 passed in 0.13s

## 13. Day 24 Deliverable

The completed Speech-to-Text Processing module provides a cleaned and normalized transcript layer for the AI screening workflow.

The system can transform raw speech-to-text output into a consistent transcript suitable for downstream screening and analysis.



