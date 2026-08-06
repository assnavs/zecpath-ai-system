"""
Day 17 - ATS System Testing

Evaluates ATS accuracy, reliability, and role adaptability.

Testing includes:
- Tech roles
- Non-tech roles
- Fresher resumes
- Senior profiles
- AI vs manual decision comparison
- Accuracy
- Precision
- Recall
- F1 Score
- Mismatch tracking
"""

import json
from pathlib import Path

from scoring.ats_scoring_engine import ATSScoringEngine


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEST_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "ats_system_test_cases.json"
)

SELECT_THRESHOLD = 70.0


# ---------------------------------------------------------
# Load Test Cases
# ---------------------------------------------------------

def load_test_cases():
    """
    Load controlled ATS system test cases.
    """

    with open(
        TEST_DATA_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return data["test_cases"]


# ---------------------------------------------------------
# Convert ATS Score to Decision
# ---------------------------------------------------------

def generate_ats_decision(overall_score):
    """
    Convert numerical ATS score into a binary
    selection decision for evaluation.

    Scores >= 70 are treated as SELECT.
    Scores below 70 are treated as REJECT.
    """

    if overall_score >= SELECT_THRESHOLD:
        return "SELECT"

    return "REJECT"


# ---------------------------------------------------------
# Metric Calculation
# ---------------------------------------------------------

def calculate_metrics(results):
    """
    Calculate system evaluation metrics.

    Positive class = SELECT
    Negative class = REJECT
    """

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for result in results:

        manual = result["manual_decision"]
        predicted = result["ats_decision"]

        if (
            manual == "SELECT"
            and predicted == "SELECT"
        ):
            true_positive += 1

        elif (
            manual == "REJECT"
            and predicted == "REJECT"
        ):
            true_negative += 1

        elif (
            manual == "REJECT"
            and predicted == "SELECT"
        ):
            false_positive += 1

        elif (
            manual == "SELECT"
            and predicted == "REJECT"
        ):
            false_negative += 1

    total = len(results)

    correct = (
        true_positive
        + true_negative
    )

    accuracy = (
        correct / total
        if total
        else 0
    )

    precision_denominator = (
        true_positive
        + false_positive
    )

    precision = (
        true_positive
        / precision_denominator
        if precision_denominator
        else 0
    )

    recall_denominator = (
        true_positive
        + false_negative
    )

    recall = (
        true_positive
        / recall_denominator
        if recall_denominator
        else 0
    )

    f1_denominator = (
        precision
        + recall
    )

    f1_score = (
        2
        * precision
        * recall
        / f1_denominator
        if f1_denominator
        else 0
    )

    mismatch_count = (
        false_positive
        + false_negative
    )

    return {
        "total_cases": total,
        "correct_predictions": correct,
        "incorrect_predictions": mismatch_count,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "accuracy": round(
            accuracy * 100,
            2,
        ),
        "precision": round(
            precision * 100,
            2,
        ),
        "recall": round(
            recall * 100,
            2,
        ),
        "f1_score": round(
            f1_score * 100,
            2,
        ),
        "mismatch_count": mismatch_count,
    }


# ---------------------------------------------------------
# Category Evaluation
# ---------------------------------------------------------

def calculate_category_accuracy(results):
    """
    Calculate accuracy for each testing category.
    """

    categories = {}

    for result in results:

        category = result["category"]

        if category not in categories:

            categories[category] = {
                "total": 0,
                "correct": 0,
            }

        categories[category]["total"] += 1

        if (
            result["manual_decision"]
            == result["ats_decision"]
        ):
            categories[category][
                "correct"
            ] += 1

    category_metrics = {}

    for category, values in categories.items():

        accuracy = (
            values["correct"]
            / values["total"]
        ) * 100

        category_metrics[category] = {
            "total_cases": values["total"],
            "correct_predictions": (
                values["correct"]
            ),
            "accuracy": round(
                accuracy,
                2,
            ),
        }

    return category_metrics


# ---------------------------------------------------------
# Run ATS Evaluation
# ---------------------------------------------------------

def evaluate_ats_system():
    """
    Run all Day 17 ATS system test cases.
    """

    test_cases = load_test_cases()

    engine = ATSScoringEngine()

    results = []

    for test_case in test_cases:

        scores = test_case["scores"]

        scoring_result = (
            engine.calculate_score(
                test_case["job_role"],
                scores["skill_match"],
                scores[
                    "experience_relevance"
                ],
                scores[
                    "education_alignment"
                ],
                scores[
                    "semantic_similarity"
                ],
            )
        )

        overall_score = scoring_result[
            "overall_score"
        ]

        ats_decision = (
            generate_ats_decision(
                overall_score
            )
        )

        manual_decision = (
            test_case["manual_decision"]
        )

        matched = (
            ats_decision
            == manual_decision
        )

        result = {
            "case_id": test_case[
                "case_id"
            ],
            "category": test_case[
                "category"
            ],
            "profile_level": test_case[
                "profile_level"
            ],
            "job_role": test_case[
                "job_role"
            ],
            "candidate": test_case[
                "candidate"
            ],
            "overall_score": (
                overall_score
            ),
            "ats_decision": (
                ats_decision
            ),
            "manual_decision": (
                manual_decision
            ),
            "matched": matched,
        }

        results.append(result)

    metrics = calculate_metrics(
        results
    )

    category_metrics = (
        calculate_category_accuracy(
            results
        )
    )

    mismatches = [
        result
        for result in results
        if not result["matched"]
    ]

    return {
        "results": results,
        "metrics": metrics,
        "category_metrics": (
            category_metrics
        ),
        "mismatches": mismatches,
    }


# ---------------------------------------------------------
# Automated Test
# ---------------------------------------------------------

def test_ats_system_evaluation():
    """
    Validate that the complete ATS evaluation
    executes correctly.
    """

    evaluation = (
        evaluate_ats_system()
    )

    metrics = evaluation["metrics"]

    assert metrics["total_cases"] == 12

    assert (
        0
        <= metrics["accuracy"]
        <= 100
    )

    assert (
        0
        <= metrics["precision"]
        <= 100
    )

    assert (
        0
        <= metrics["recall"]
        <= 100
    )

    assert (
        0
        <= metrics["f1_score"]
        <= 100
    )

    categories = (
        evaluation[
            "category_metrics"
        ]
    )

    assert "Tech Role" in categories

    assert (
        "Non-Tech Role"
        in categories
    )

    assert (
        "Fresher Resume"
        in categories
    )

    assert (
        "Senior Profile"
        in categories
    )

    return evaluation


# ---------------------------------------------------------
# Terminal Report
# ---------------------------------------------------------

def print_evaluation_report(
    evaluation
):

    print(
        "\n===== Day 17 ATS System Testing =====\n"
    )

    print(
        "----- Candidate Test Results -----\n"
    )

    for result in evaluation["results"]:

        status = (
            "MATCH"
            if result["matched"]
            else "MISMATCH"
        )

        print(
            f'{result["case_id"]} | '
            f'{result["category"]} | '
            f'{result["job_role"]} | '
            f'Score: {result["overall_score"]} | '
            f'ATS: {result["ats_decision"]} | '
            f'Manual: {result["manual_decision"]} | '
            f'{status}'
        )

    print(
        "\n----- Accuracy Metrics -----\n"
    )

    print(
        json.dumps(
            evaluation["metrics"],
            indent=4,
        )
    )

    print(
        "\n----- Category Accuracy -----\n"
    )

    print(
        json.dumps(
            evaluation[
                "category_metrics"
            ],
            indent=4,
        )
    )

    print(
        "\n----- Mismatch Cases -----\n"
    )

    mismatches = evaluation[
        "mismatches"
    ]

    if mismatches:

        for mismatch in mismatches:

            print(
                f'{mismatch["case_id"]} | '
                f'{mismatch["candidate"]} | '
                f'{mismatch["job_role"]} | '
                f'Score: '
                f'{mismatch["overall_score"]} | '
                f'ATS: '
                f'{mismatch["ats_decision"]} | '
                f'Manual: '
                f'{mismatch["manual_decision"]}'
            )

    else:

        print(
            "No mismatch cases detected."
        )

    print(
        "\nAll Day 17 ATS System "
        "Testing completed successfully!"
    )


# ---------------------------------------------------------
# Direct Execution
# ---------------------------------------------------------

if __name__ == "__main__":

    evaluation_result = (
        test_ats_system_evaluation()
    )

    print_evaluation_report(
        evaluation_result
    )