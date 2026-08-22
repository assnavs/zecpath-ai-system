# Day 23 – Transcript Data Architecture

## 1. Objective

The Transcript Data Architecture defines how voice conversations are converted into structured, AI-processable data for automated screening interactions.

The architecture provides a standardized structure for transcript storage, metadata, normalization, and screening interaction records.

## 2. Transcript Storage Structure

The voice transcript schema is stored at:

`data/voice_transcript_schema.json`

The schema defines the standard structure required for transcript records.

## 3. Metadata Standards

Each transcript record uses standardized metadata fields:

- Candidate ID
- Job ID
- Question ID
- Timestamp
- Confidence level

Additional transcript fields include:

- Speaker
- Transcript text

## 4. Confidence Level

The confidence level represents the confidence associated with the transcript information.

The configured range is:

- Minimum: 0.0
- Maximum: 1.0

## 5. Speaker Standards

Transcript records identify the speaker using one of the following values:

- candidate
- interviewer

This allows downstream AI components to distinguish candidate responses from interviewer questions.

## 6. Transcript Normalization

The transcript normalization utility is implemented at:

`utils/transcript_normalizer.py`

The normalization process includes:

- Removing leading and trailing whitespace
- Collapsing repeated whitespace
- Normalizing line breaks
- Preserving the original meaning of the transcript
- Lowercase conversion for matching operations only

## 7. Screening Interaction Structure

The screening interaction schema is stored at:

`data/screening_interaction_schema.json`

It provides a structured representation of individual AI screening interactions.

Each interaction contains:

- Candidate ID
- Job ID
- Question ID
- Timestamp
- Confidence level
- Speaker
- Normalized transcript text

## 8. AI-Processable Data Structure

The architecture converts raw transcript information into structured records that can be consumed by future AI screening and conversation components.

The standardized metadata makes it possible to associate each response with:

- The candidate
- The job
- The screening question
- The conversation timestamp
- The transcript confidence level

## 9. Testing

The Day 23 automated test suite validates:

- Transcript schema existence
- Screening interaction schema existence
- Required metadata fields
- Confidence-level range
- Valid speaker values
- Transcript text normalization
- Line-break normalization
- Matching normalization
- Screening interaction normalization

### Test Result

All Day 23 Transcript Data Architecture tests passed successfully.

**Result: 9/9 tests passed.**

## 10. Day 23 Deliverables

The completed Day 23 work provides:

- Voice transcript schema
- AI screening interaction schema
- Standardized transcript metadata
- Transcript normalization utility
- AI-processable screening interaction structure
- Automated validation tests
