import json
import os

from parsers.resume_section_classifier import ResumeSectionClassifier


sample_resume = """
John Doe
Data Science Engineer

SKILLS
Python
SQL
Machine Learning
Power BI

WORK EXPERIENCE
Data Science Intern
ABC Technologies
Jan 2025 - Present

EDUCATION
Bachelor of Computer Applications
XYZ University

PROJECTS
AI Resume Parser
Job Recommendation System

CERTIFICATIONS
Python Essentials
Google Data Analytics
"""


def main():

    classifier = ResumeSectionClassifier()

    sections = classifier.classify_sections(sample_resume)

    print("\nResume Section Classification\n")

    for section, content in sections.items():
        print("=" * 50)
        print(section.upper())
        print(content)

    os.makedirs("data/labeled_resume_samples", exist_ok=True)

    output_path = "data/labeled_resume_samples/sample_resume_sections.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(sections, file, indent=4, ensure_ascii=False)

    print(f"\nStructured output saved to: {output_path}")


if __name__ == "__main__":
    main()