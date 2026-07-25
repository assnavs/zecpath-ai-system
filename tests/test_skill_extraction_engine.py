"""
Unit Test for Skill Extraction Engine
"""

import json

from parsers.skill_extraction_engine import SkillExtractionEngine


def test_skill_extraction():

    sample_resume = """
    Data Analyst

    Skills:
    Python
    SQL Server
    Microsoft Excel
    PowerBI
    Tableau Desktop
    Communication
    Leadership

    Built multiple MERN applications.
    """

    engine = SkillExtractionEngine()

    result = engine.extract(sample_resume)

    print("\n===== Skill Extraction Result =====\n")
    print(json.dumps(result, indent=4))

    assert result["total_skills"] > 0

    extracted = [item["skill"] for item in result["skills"]]

    assert "Python" in extracted
    assert "SQL" in extracted
    assert "Excel" in extracted
    assert "Power BI" in extracted
    assert "Tableau" in extracted
    assert "Communication" in extracted
    assert "Leadership" in extracted
    assert "React" in extracted
    assert "MongoDB" in extracted
    assert "Node.js" in extracted

    print("\nAll Skill Extraction Tests Passed.\n")


if __name__ == "__main__":
    test_skill_extraction()