import json

from scoring.semantic_matching_engine import SemanticMatchingEngine


def test_semantic_matching_engine():
    """
    Unit test for Semantic Matching Engine.
    """

    engine = SemanticMatchingEngine()

    resume_skills = """
    Python
    Machine Learning
    SQL
    Pandas
    Scikit-learn
    """

    jd_skills = """
    Python
    SQL
    Machine Learning
    Data Analysis
    """

    resume_experience = """
    Developed machine learning models
    using Python and Scikit-learn for
    predictive analytics.
    """

    jd_experience = """
    Experience in developing machine
    learning solutions using Python.
    """

    resume_projects = """
    Resume Screening System using NLP
    and Machine Learning.
    """

    jd_projects = """
    AI-based Resume Screening platform
    with NLP capabilities.
    """

    result = engine.calculate_overall_similarity(
        resume_skills,
        jd_skills,
        resume_experience,
        jd_experience,
        resume_projects,
        jd_projects,
    )

    print("\nSemantic Matching Result:\n")
    print(json.dumps(result, indent=4))

    assert "overall_similarity" in result
    assert "match_level" in result

    assert result["overall_similarity"] >= 0
    assert result["overall_similarity"] <= 100

    print("\nAll Semantic Matching tests passed successfully!")


if __name__ == "__main__":
    test_semantic_matching_engine()