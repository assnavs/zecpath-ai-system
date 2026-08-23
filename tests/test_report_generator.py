from screening_ai.report_generator import AIScreeningReportGenerator


def sample_report_data():
    return {
        "candidate_name": "Test Candidate",
        "job_role": "Data Analyst",
        "salary_expectation": "6 LPA",
        "availability": "Immediate",
        "skill_confirmations": [
            "Python",
            "SQL",
            "Power BI"
        ],
        "answers": [
            {
                "question_id": "Q1",
                "question": "Tell me about your skills.",
                "answer": "I know Python, SQL and Power BI.",
                "intent": "skills"
            }
        ],
        "ats_evaluation": {
            "overall_score": 85,
            "recommendation": "Strong Candidate"
        },
        "screening_evaluation": {
            "final_screening_score": 82
        },
        "confidence_evaluation": {
            "confidence_score": 80,
            "communication_strength": "strong",
            "signals": {}
        },
        "shortlisting": {
            "decision": "Shortlisted"
        }
    }


def test_report_generator_creation():
    generator = AIScreeningReportGenerator()

    assert generator is not None


def test_key_answer_extraction():
    generator = AIScreeningReportGenerator()

    answers = sample_report_data()["answers"]

    result = generator.extract_key_answers(
        answers
    )

    assert len(result) == 1
    assert result[0]["question_id"] == "Q1"
    assert result[0]["intent"] == "skills"


def test_strength_detection():
    generator = AIScreeningReportGenerator()

    result = generator.identify_strengths(
        sample_report_data()
    )

    assert "Strong ATS evaluation score" in result
    assert (
        "Relevant skills confirmed during screening"
        in result
    )


def test_missing_data_detection():
    generator = AIScreeningReportGenerator()

    data = sample_report_data()

    data["salary_expectation"] = None

    result = generator.identify_missing_data(
        data
    )

    assert "Salary expectation" in result


def test_risk_detection():
    generator = AIScreeningReportGenerator()

    data = sample_report_data()

    data["confidence_evaluation"] = {
        "confidence_score": 40,
        "signals": {}
    }

    result = generator.identify_risks(
        data
    )

    assert (
        "Communication signals require improvement"
        in result
    )


def test_recommendation_from_shortlisting():
    generator = AIScreeningReportGenerator()

    result = generator.determine_recommendation(
        sample_report_data()
    )

    assert result == "Shortlisted"


def test_ats_based_recommendation():
    generator = AIScreeningReportGenerator()

    data = sample_report_data()

    data["shortlisting"] = {}

    result = generator.determine_recommendation(
        data
    )

    assert result == "Shortlisted"


def test_complete_report_generation():
    generator = AIScreeningReportGenerator()

    result = generator.generate_report(
        sample_report_data()
    )

    assert result["report_type"] == (
        "AI Screening Report"
    )

    assert "candidate" in result
    assert "summary" in result
    assert "highlights" in result
    assert "evaluations" in result
    assert "shortlisting" in result
    assert "recommendation" in result


def test_report_contains_required_summary_sections():
    generator = AIScreeningReportGenerator()

    result = generator.generate_report(
        sample_report_data()
    )

    summary = result["summary"]

    assert "key_answers" in summary
    assert "strengths" in summary
    assert "risks" in summary
    assert "missing_data" in summary


def test_text_report_generation():
    generator = AIScreeningReportGenerator()

    report = generator.generate_report(
        sample_report_data()
    )

    result = generator.generate_text_report(
        report
    )

    assert "AI SCREENING REPORT" in result
    assert "Test Candidate" in result
    assert "Shortlisted" in result
    assert "Python" in result


def test_json_export(tmp_path):
    generator = AIScreeningReportGenerator()

    report = generator.generate_report(
        sample_report_data()
    )

    output_path = (
        tmp_path / "screening_report.json"
    )

    result = generator.export_json(
        report,
        str(output_path)
    )

    assert output_path.exists()
    assert result == str(output_path)
