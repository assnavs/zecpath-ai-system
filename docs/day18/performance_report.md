# ATS Performance Report

## Day 18 – Optimization & Performance Tuning

## 1. Overview

This report documents the performance measurements collected after the Day 18 ATS optimization work.

The evaluation measured:

- Resume text-cleaning time
- PDF text-extraction time
- Semantic processing time
- Repeated semantic-engine initialization time
- Tracked peak memory during repeated lightweight processing

The measurements were generated directly from the Day 18 performance test executed in the project environment.

---

# 2. Performance Test Status

All tested optimization components completed successfully.

```text
Noisy resume cleaning: PASSED
Header/Profile detection: PASSED
Resume normalization: PASSED
PDF extraction: PASSED
Semantic model reuse: PASSED
Semantic batch processing: PASSED
Memory stability test: PASSED
```

Final status:

```text
All Day 18 Optimization and Performance tests passed successfully!
```

---

# 3. Measured Performance Summary

| Measurement | Result |
|---|---:|
| Text Cleaning Time | 0.001457 sec |
| PDF Extraction Time | 0.105023 sec |
| Semantic Processing Time | 0.183752 sec |
| Second Semantic Engine Initialization | 0.001425 sec |
| Peak Tracked Memory | 0.0040 MB |

These values represent measurements from the successful Day 18 test run.

---

# 4. Text Cleaning Performance

Measured result:

```text
0.001457 seconds
```

The cleaning process included handling of:

- Excessive whitespace
- Multiple blank lines
- Bullet characters
- Incorrectly decoded bullet text
- Decorative separators
- Control characters
- Unicode normalization
- Common section headings

The noisy-resume test completed successfully.

---

# 5. PDF Extraction Performance

Measured result:

```text
0.105023 seconds
```

The test used the available sample resume PDF.

The optimized extraction process:

1. Opens the PDF.
2. Processes pages sequentially.
3. Stores extracted page text in a list.
4. Joins the page content once.
5. Releases the PDF resource after processing.

The extraction test successfully returned non-empty resume text.

---

# 6. Semantic Processing Performance

Measured overall semantic-processing time:

```text
0.183752 seconds
```

The semantic operation compared:

- Skills
- Experience
- Projects

between candidate resume information and job-description information.

All six text inputs were encoded using a batch operation.

The semantic batch-processing test passed successfully.

---

# 7. Semantic Model Reuse

The first Semantic Matching Engine instance initializes the SentenceTransformer model when necessary.

A second engine instance was then created.

Measured second initialization time:

```text
0.001425 seconds
```

The test also explicitly verified that:

```text
first_engine.model is second_engine.model
```

evaluated successfully.

This confirms that both engine instances referenced the same loaded model object within the process.

---

# 8. Memory Stability Test

The performance test repeatedly executed:

- Text cleaning
- Resume section classification

for 100 iterations while Python memory allocation was tracked using `tracemalloc`.

Measured peak tracked memory:

```text
0.0040 MB
```

The test completed successfully without processing failure.

This measurement represents Python allocations tracked during the measured test section and should not be interpreted as the total memory consumption of the entire ATS application or SentenceTransformer model.

---

# 9. Post-Optimization Performance Measurements

The measured results can be summarized as:

```text
Text Cleaning
    0.001457 sec

PDF Extraction
    0.105023 sec

Semantic Batch Processing
    0.183752 sec

Second Semantic Engine Initialization
    0.001425 sec

Peak Tracked Memory
    0.0040 MB
```

---

# 10. Interpretation

The measurements demonstrate that the optimized components execute successfully within the current development environment.

In particular:

- Text normalization completed quickly for the controlled noisy-resume sample.
- PDF extraction successfully processed the sample resume.
- Semantic comparison successfully handled six text inputs through batch encoding.
- Repeated Semantic Matching Engine creation reused the existing model.
- Repeated text-processing operations completed with low tracked Python allocation in the measured section.

---

# 11. Regression Test

After optimization, the existing Semantic Matching Engine test was rerun.

Results:

| Component | Result |
|---|---:|
| Skills Similarity | 76.63% |
| Experience Similarity | 66.39% |
| Projects Similarity | 84.05% |
| Overall Similarity | 75.69% |
| Match Level | Good Match |

Test status:

```text
All Semantic Matching tests passed successfully!
```

This confirms that the optimization did not break the previously tested semantic-matching behavior.

---

# 12. Benchmark Limitation

The Day 18 measurements are post-optimization measurements.

An equivalent controlled pre-optimization benchmark was not recorded during this test cycle.

Therefore, the results should not be expressed as unsupported claims such as:

```text
"50% faster"
"80% performance improvement"
"2x faster"
```

without additional before-and-after benchmarking.

The current measurements instead establish a useful performance baseline for future comparison.

---

# 13. Future Benchmarking

A future benchmark can measure both implementations under identical conditions using:

```text
Same Resume
Same Job Description
Same Machine
Same Model
Same Number of Iterations
Same Runtime Conditions
```

Metrics could include:

- Mean processing time
- Median processing time
- P95 latency
- Model cold-start time
- Warm-model processing time
- Peak process memory
- Large-resume processing time
- Multi-resume throughput

This would allow quantitative before-and-after improvement percentages to be calculated reliably.

---

# 14. Conclusion

Day 18 performance testing successfully validated the optimized ATS components.

The test produced measurable post-optimization baselines for text cleaning, PDF extraction, semantic processing, repeated engine initialization, and tracked Python memory allocation.

The existing semantic matching regression test also passed, demonstrating that the optimization preserved previously tested functionality.

These measurements establish a baseline that can be reused for future performance and scalability comparisons.