# ATS Stability Improvements

## Day 18 – Optimization & Performance Tuning

## 1. Overview

Day 18 included stability improvements designed to make ATS processing more consistent when handling different resume formats, noisy extracted text, repeated semantic operations, and structured candidate information.

The stability work focused on improving existing modules while maintaining compatibility with previously tested ATS functionality.

---

# 2. Stability Areas Addressed

The following areas were improved:

```text
PDF resource handling
Text normalization
Noisy resume processing
Resume header classification
Section heading recognition
Duplicate value handling
Null-value handling
Semantic model reuse
Batch embedding processing
Memory handling
Regression compatibility
```

---

# 3. PDF Resource Stability

PDF processing now uses a context-managed document workflow.

Conceptually:

```text
Open PDF
   ↓
Extract Pages
   ↓
Build Text
   ↓
Close PDF Resource
```

This ensures that the PDF document is properly released after processing, including when extraction logic exits its normal scope.

Empty page text is also safely ignored.

---

# 4. Safe PDF Failure Handling

PDF extraction remains protected by exception handling.

If extraction fails, the system:

- Records the failure through logging.
- Returns an empty string.
- Avoids terminating the entire ATS pipeline from the extraction function.

This provides predictable behavior for downstream components.

---

# 5. Noisy Resume Stability

Resume extraction can produce inconsistent characters and formatting.

The improved cleaner handles:

- Windows and Unix line-ending differences
- Control characters
- Multiple spaces
- Excessive blank lines
- Multiple bullet symbols
- Incorrectly decoded bullets
- Decorative repeated characters
- Unicode representation differences

This produces more consistent input for downstream ATS components.

---

# 6. Consistent Section Headings

Common section-heading variations are standardized or recognized.

For example:

```text
TECHNICAL SKILLS
Technical Skills
technical skills
```

can be processed more consistently.

This reduces dependence on one exact capitalization or formatting style.

---

# 7. Resume Header Stability

Previously, resume content before the first recognized section heading could be classified as:

```text
UNKNOWN
```

This could incorrectly place important information such as:

```text
Candidate Name
Current Designation
Professional Title
Contact Header
```

into an unknown section.

The classifier now starts with:

```text
profile
```

as the initial section.

This means header information is preserved under a meaningful resume category.

---

# 8. Reduced UNKNOWN Classification

The updated behavior is:

```text
Resume Starts
     ↓
Header Information
     ↓
PROFILE
     ↓
Recognized Heading
     ↓
Corresponding Resume Section
```

The Day 18 test verified:

```text
"profile" exists
"John Doe" exists in profile
"Data Scientist" exists in profile
"unknown" does not exist
```

The test passed successfully.

---

# 9. Resume Normalization Stability

The Resume Normalizer was improved to safely process:

- Strings
- Lists
- Tuples
- Sets
- Nested dictionaries
- Null values
- Personal attributes configured for masking

This helps reduce inconsistent structured data before candidate evaluation.

---

# 10. Duplicate Handling

Normalized list values use order-preserving duplicate detection.

Example input:

```text
Python
Python
SQL
 Python
```

Normalized result:

```text
python
sql
```

This prevents repeated extracted skills from unnecessarily appearing multiple times in normalized candidate information.

---

# 11. Personal Attribute Masking

The normalizer continues to support masking configured attributes.

Example:

```text
email → [MASKED]
phone → [MASKED]
```

The Day 18 test confirmed that configured personal information was masked correctly.

---

# 12. Semantic Model Stability

The SentenceTransformer model is now shared across Semantic Matching Engine instances within the same Python process.

This avoids unnecessary repeated model creation.

The test confirmed:

```text
first_engine.model
    IS
second_engine.model
```

Result:

```text
Semantic model reuse: PASSED
```

---

# 13. Batch Semantic Processing Stability

Skills, experience, and project text pairs are processed together in one embedding batch during overall semantic similarity calculation.

The workflow is:

```text
6 Text Inputs
     ↓
Single Batch Encode
     ↓
6 Normalized Embeddings
     ↓
3 Pair Comparisons
     ↓
Overall Similarity
```

This reduces repeated model invocation while preserving the existing semantic scoring output structure.

---

# 14. Similarity Output Stability

The optimized engine continues to return:

```text
skills_similarity
experience_similarity
projects_similarity
overall_similarity
match_level
```

This preserves compatibility with code that already consumes the semantic matching result.

---

# 15. Regression Stability

After optimization, the existing semantic matching test was rerun.

The result remained:

```text
skills_similarity: 76.63
experience_similarity: 66.39
projects_similarity: 84.05
overall_similarity: 75.69
match_level: Good Match
```

Final result:

```text
All Semantic Matching tests passed successfully!
```

This regression test provides evidence that the Day 18 semantic changes preserved the previously tested output behavior.

---

# 16. Memory Stability

A controlled memory test repeatedly executed resume cleaning and section classification 100 times.

The operations completed successfully.

Measured peak Python allocation during the tracked section:

```text
0.0040 MB
```

The measurement was collected using `tracemalloc`.

It represents tracked Python allocations for that specific test section rather than total application or machine memory usage.

---

# 17. Stability Test Summary

| Stability Check | Status |
|---|---|
| Noisy resume cleaning | Passed |
| Profile/header detection | Passed |
| Resume normalization | Passed |
| PDF extraction | Passed |
| Semantic model reuse | Passed |
| Semantic batch processing | Passed |
| Repeated processing memory test | Passed |
| Existing semantic regression test | Passed |

---

# 18. Operational Considerations

The current optimization improves development-stage stability, but production deployment would require additional validation.

Future stability testing can include:

- Corrupted PDF files
- Password-protected PDFs
- Very large resumes
- Image-only resumes
- Empty resumes
- Unusual Unicode characters
- Very long skill lists
- Multiple simultaneous requests
- Model-loading failures
- Large batch processing
- Persistent memory monitoring

These tests would provide broader evidence for production readiness.

---

# 19. Conclusion

Day 18 stability improvements strengthened ATS handling across PDF extraction, text cleaning, normalization, resume section classification, semantic processing, and repeated operations.

A key improvement was the classification of resume header information as PROFILE instead of UNKNOWN.

Shared semantic model reuse and batch embedding processing reduced unnecessary repeated operations, while regression testing confirmed that previously tested semantic matching behavior remained functional.

All Day 18 optimization and stability tests completed successfully.