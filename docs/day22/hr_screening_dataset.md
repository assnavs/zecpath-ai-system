# Day 22 – HR Screening Dataset Creation

## 1. Objective

The HR Screening Dataset provides a structured, AI-ready question bank for automated HR screening calls.

The dataset is designed to support multiple job roles and organize screening questions into reusable categories.

## 2. Question Categories

The dataset includes the following screening categories:

- Introduction
- Education
- Experience
- Skills
- Location
- Salary
- Notice Period

## 3. Supported Job Roles

The current dataset contains screening questions for:

- Data Scientist
- Data Analyst
- Software Engineer

Each role contains questions covering all required screening categories.

## 4. Question Metadata

Each question is stored as an AI-ready question object containing:

- Question ID
- Category
- Question text
- Expected answer type
- Mandatory or optional status
- Scoring importance

## 5. Expected Answer Types

The dataset currently supports:

- Text
- Number
- Multiple choice

This structure allows the questions to be processed consistently by future AI screening and conversation modules.

## 6. Mandatory and Optional Questions

Questions are tagged as either:

- Mandatory
- Optional

Mandatory questions represent information required for the screening process, while optional questions provide additional candidate information.

## 7. Scoring Importance

Each question contains a scoring importance value from 1 to 3.

- 1 – Lower importance
- 2 – Moderate importance
- 3 – Higher importance

This allows future screening logic to prioritize important responses.

## 8. Dataset Structure

The dataset is stored at:

`data/hr_screening_dataset.json`

The structure contains:

HR Screening Dataset
|
+-- Dataset Metadata
+-- Question Categories
+-- Supported Answer Types
+-- Roles
    |
    +-- Data Scientist
    +-- Data Analyst
    +-- Software Engineer
        |
        +-- Introduction
        +-- Education
        +-- Experience
        +-- Skills
        +-- Location
        +-- Salary
        +-- Notice Period

## 9. AI Conversation Readiness

The question objects are structured so they can be consumed by future automated HR screening and conversational AI components.

Each question has a unique identifier and standardized metadata, making the dataset reusable across different screening workflows.

## 10. Testing

The Day 22 automated tests validate:

- Dataset existence
- Required question categories
- Multiple job roles
- Question object structure
- Mandatory and optional question tagging
- Scoring importance
- AI-ready question object format

### Test Result

All Day 22 HR Screening Dataset tests passed successfully.

## 11. Day 22 Deliverables

The completed Day 22 work provides:

- HR screening question dataset
- Question category mapping
- AI conversation-ready question objects
- Reusable question metadata structure
- Multi-role screening question support
