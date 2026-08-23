# Day 25 – Answer Intent and Understanding Engine

## 1. Objective

The Answer Intent and Understanding Engine processes candidate responses from the screening workflow and converts them into structured semantic information.

The engine identifies the likely intent of a candidate answer, detects vague or off-topic responses, and extracts basic information relevant to the identified intent.

## 2. Processing Capabilities

The Day 25 engine supports:

- Answer intent classification
- Answer text normalization
- Skills intent detection
- Experience intent detection
- Availability intent detection
- Salary expectation intent detection
- Off-topic response detection
- Missing or vague answer detection
- Skill extraction
- Experience information extraction
- Salary information extraction
- Structured semantic output

## 3. Answer Understanding Flow

```text
Candidate Answer
        |
        v
Text Normalization
        |
        v
Intent Classification
        |
        +----------------------+
        |                      |
        v                      v
Off-Topic Detection      Missing/Vague Detection
        |                      |
        +----------+-----------+
                   |
                   v
        Information Extraction
                   |
                   v
        Structured Semantic Object
```

## 4. Text Normalization

The engine normalizes candidate answers before processing.

Normalization includes:

- Removing leading and trailing whitespace
- Converting multiple whitespace characters into single spaces
- Converting text to lowercase for matching

This provides a consistent representation for keyword-based intent detection.

## 5. Intent Classification

The engine classifies candidate responses into supported intent categories.

### Skills

Used when the candidate discusses technical or professional skills.

Example:

"I have skills in Python, SQL and Power BI"

Expected intent:

`skills`

### Experience

Used when the candidate discusses previous work or professional experience.

Example:

"I have three years of experience in data analysis"

Expected intent:

`experience`

### Availability

Used when the candidate discusses joining or availability.

Example:

"I am available to join immediately"

Expected intent:

`availability`

### Salary Expectation

Used when the candidate discusses expected compensation.

Example:

"My expected salary is 6 LPA"

Expected intent:

`salary_expectation`

## 6. Keyword-Based Intent Scoring

Intent classification uses configured keywords stored in:

`data/answer_intent_patterns.json`

The engine calculates a matching score for each configured intent.

The intent with the highest matching score is selected as the primary intent.

If no configured keywords match, the engine returns:

`unknown`

with a confidence value of `0.0`.

## 7. Confidence Calculation

The engine generates a confidence value based on the number of matching intent keywords.

The confidence is capped at `0.95`.

This provides a consistent confidence value for downstream processing.

## 8. Off-Topic Detection

The engine detects responses that contain configured off-topic keywords.

For example, a response such as:

"I watched a cricket match yesterday"

can be identified as an off-topic response.

The structured result marks:

- `off_topic` as `True`
- `response_status` as `off_topic`

## 9. Missing or Vague Answer Detection

The engine identifies empty, extremely short, or vague responses.

Examples include:

- Yes
- No
- Maybe
- Not sure
- I don't know
- None
- Nothing
- Some
- Okay
- Fine

Such responses are marked as missing or vague.

The structured result contains:

`missing_or_vague: True`

and:

`response_status: missing_or_vague`

## 10. Skill Extraction

For answers classified with the `skills` intent, the engine checks for known technical skills.

Supported examples include:

- Python
- SQL
- Java
- JavaScript
- TypeScript
- C++
- C#
- HTML
- CSS
- Excel
- Power BI
- Tableau
- Machine Learning
- Deep Learning
- Pandas
- NumPy
- Scikit-learn
- Docker
- Kubernetes

The extracted skills are stored in the semantic data section of the response.

## 11. Experience Extraction

For answers classified with the `experience` intent, the engine extracts numerical experience values expressed in years.

Example:

"I have 3 years of experience in data analysis"

produces:

`years: [3]`

The original normalized answer is also retained as experience details.

## 12. Salary Extraction

For answers classified with the `salary_expectation` intent, the engine extracts numerical salary values.

The implementation supports salary expressions involving:

- LPA
- Lakhs
- Lakh
- INR
- Rs.
- ₹

Example:

"I expect around 6 LPA"

produces a salary value containing:

`6`

## 13. Structured Semantic Object

The `understand()` method combines the processing stages into a structured result.

The result contains:

- Raw answer text
- Normalized answer text
- Detected intent
- Confidence
- Off-topic status
- Missing/vague status
- Response status
- Semantic data

This structure can be used by downstream AI screening components.

## 14. Answer Understanding Engine Alias

The implementation also provides:

`AnswerUnderstandingEngine`

as an alias derived from `AnswerIntentEngine`.

This allows the same implementation to be represented using answer-understanding terminology within the screening architecture.

## 15. Implementation

Main implementation:

`screening_ai/answer_intent_engine.py`

Intent configuration:

`data/answer_intent_patterns.json`

Automated tests:

`tests/test_answer_intent_engine.py`

## 16. JSON Encoding Handling

During testing, the intent-pattern JSON file contained a UTF-8 BOM.

The JSON loading implementation was updated to use:

`utf-8-sig`

This allows the engine to correctly read the JSON configuration while supporting UTF-8 BOM encoded files.

## 17. Testing

The Day 25 automated test suite validates:

- Pattern file availability
- Skills intent classification
- Experience intent classification
- Availability intent classification
- Salary expectation classification
- Skill extraction
- Experience extraction
- Salary extraction
- Off-topic detection
- Vague answer detection
- Structured semantic object generation
- Empty answer handling
- Multiple answer types

## 18. Test Result

All Day 25 Answer Intent Engine tests passed successfully.

```text
13 passed in 0.07s
```

## 19. Day 25 Deliverable

The completed Answer Intent and Understanding Engine provides a structured interpretation layer for candidate screening responses.

It converts candidate answers into normalized, classified, and structured semantic information that can be used by downstream screening and analysis components.
