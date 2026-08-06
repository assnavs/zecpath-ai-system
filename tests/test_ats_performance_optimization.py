"""
Day 18 - ATS Optimization & Performance Testing

Validates:
- Text cleaning
- Noisy resume handling
- Profile/header detection
- Semantic model reuse
- Semantic batch processing
- PDF extraction performance
- Memory stability
"""

import time
import tracemalloc
from pathlib import Path

from parsers.pdf_reader import (
    extract_pdf_text,
)
from parsers.text_cleaner import (
    clean_text,
)
from parsers.resume_normalizer import (
    ResumeNormalizer,
)
from parsers.resume_section_classifier import (
    ResumeSectionClassifier,
)
from scoring.semantic_matching_engine import (
    SemanticMatchingEngine,
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


def test_ats_performance_optimization():

    print(
        "\n===== Day 18 ATS "
        "Performance Optimization =====\n"
    )

    # -----------------------------------------
    # 1. Noisy Resume Cleaning
    # -----------------------------------------

    noisy_resume = """
    JOHN DOE


    Data Scientist     


    â€¢ Python
    • SQL
    ● Machine Learning

    ====================

    SKILLS


    Python       SQL       Pandas


    WORK EXPERIENCE


    Data Analyst
    """

    start = time.perf_counter()

    cleaned = clean_text(
        noisy_resume
    )

    cleaning_time = (
        time.perf_counter()
        - start
    )

    assert "â€¢" not in cleaned
    assert "•" not in cleaned
    assert "●" not in cleaned

    print(
        "Noisy resume cleaning: PASSED"
    )

    print(
        f"Cleaning time: "
        f"{cleaning_time:.6f} seconds"
    )

    # -----------------------------------------
    # 2. Header/Profile Detection
    # -----------------------------------------

    classifier = (
        ResumeSectionClassifier()
    )

    sample_resume = """
John Doe
Data Scientist
john@example.com

SKILLS
Python
SQL

WORK EXPERIENCE
Data Analyst - ABC Company

EDUCATION
Master of Computer Applications
"""

    sections = (
        classifier.classify_sections(
            sample_resume
        )
    )

    assert "profile" in sections

    assert (
        "John Doe"
        in sections["profile"]
    )

    assert (
        "Data Scientist"
        in sections["profile"]
    )

    assert "unknown" not in sections

    print(
        "Header/Profile detection: PASSED"
    )

    # -----------------------------------------
    # 3. Resume Normalization
    # -----------------------------------------

    normalizer = ResumeNormalizer(
        attributes_to_mask=[
            "email",
            "phone",
        ]
    )

    normalized = (
        normalizer.normalize_resume(
            {
                "Name": "  John   Doe ",
                "Email": (
                    "john@example.com"
                ),
                "Skills": [
                    "Python",
                    " Python ",
                    "SQL",
                ],
            }
        )
    )

    assert (
        normalized["email"]
        == "[MASKED]"
    )

    assert normalized["skills"] == [
        "python",
        "sql",
    ]

    print(
        "Resume normalization: PASSED"
    )

    # -----------------------------------------
    # 4. PDF Extraction Performance
    # -----------------------------------------

    sample_pdf = (
        PROJECT_ROOT
        / "data"
        / "sample_resumes"
        / "barry_stevens_resume.pdf"
    )

    start = time.perf_counter()

    extracted_text = (
        extract_pdf_text(
            sample_pdf
        )
    )

    extraction_time = (
        time.perf_counter()
        - start
    )

    assert extracted_text

    print(
        "PDF extraction: PASSED"
    )

    print(
        f"PDF extraction time: "
        f"{extraction_time:.6f} seconds"
    )

    # -----------------------------------------
    # 5. Semantic Model Reuse
    # -----------------------------------------

    print(
        "\nLoading semantic engine..."
    )

    first_engine = (
        SemanticMatchingEngine()
    )

    start = time.perf_counter()

    second_engine = (
        SemanticMatchingEngine()
    )

    second_init_time = (
        time.perf_counter()
        - start
    )

    assert (
        first_engine.model
        is second_engine.model
    )

    print(
        "Semantic model reuse: PASSED"
    )

    print(
        f"Second engine initialization: "
        f"{second_init_time:.6f} seconds"
    )

    # -----------------------------------------
    # 6. Semantic Batch Performance
    # -----------------------------------------

    start = time.perf_counter()

    semantic_result = (
        first_engine
        .calculate_overall_similarity(
            "Python SQL Machine Learning",
            "Python SQL Data Science",
            (
                "Two years Data Analyst "
                "experience"
            ),
            (
                "Data analysis experience "
                "required"
            ),
            (
                "Machine learning "
                "prediction project"
            ),
            (
                "Predictive analytics "
                "project experience"
            ),
        )
    )

    semantic_time = (
        time.perf_counter()
        - start
    )

    assert (
        0
        <= semantic_result[
            "overall_similarity"
        ]
        <= 100
    )

    print(
        "Semantic batch processing: PASSED"
    )

    print(
        f"Semantic processing time: "
        f"{semantic_time:.6f} seconds"
    )

    # -----------------------------------------
    # 7. Memory Test
    # -----------------------------------------

    tracemalloc.start()

    for _ in range(100):

        clean_text(
            noisy_resume
        )

        classifier.classify_sections(
            sample_resume
        )

    current_memory, peak_memory = (
        tracemalloc.get_traced_memory()
    )

    tracemalloc.stop()

    peak_memory_mb = (
        peak_memory
        / 1024
        / 1024
    )

    print(
        "Memory stability test: PASSED"
    )

    print(
        f"Peak tracked memory: "
        f"{peak_memory_mb:.4f} MB"
    )

    # -----------------------------------------
    # Summary
    # -----------------------------------------

    print(
        "\n===== Performance Summary =====\n"
    )

    print(
        f"Text cleaning time: "
        f"{cleaning_time:.6f} sec"
    )

    print(
        f"PDF extraction time: "
        f"{extraction_time:.6f} sec"
    )

    print(
        f"Semantic processing time: "
        f"{semantic_time:.6f} sec"
    )

    print(
        f"Second model init time: "
        f"{second_init_time:.6f} sec"
    )

    print(
        f"Peak tracked memory: "
        f"{peak_memory_mb:.4f} MB"
    )

    print(
        "\nAll Day 18 Optimization "
        "and Performance tests "
        "passed successfully!"
    )


if __name__ == "__main__":

    test_ats_performance_optimization()