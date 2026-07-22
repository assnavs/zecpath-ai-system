"""
Job Description Parser

Reads job descriptions from a DOCX file and converts them into
structured AI-readable job requirement objects.
"""

import re
from docx import Document

from parsers.jd_cleaner import clean_job_description
from parsers.skill_normalizer import normalize_role, normalize_skill


def read_docx(file_path):
    """
    Read all text from a DOCX document.
    """

    document = Document(file_path)

    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )

    return clean_job_description(text)


def split_job_descriptions(text):
    """
    Split the document into individual job descriptions.
    """

    jobs = re.split(r"\n(?=\d+\.\s)", text)

    return [job.strip() for job in jobs if job.strip()]


def extract_job_data(job_text):
    """
    Extract structured information from one job description.
    """

    lines = [line.strip() for line in job_text.split("\n") if line.strip()]

    job = {
        "job_title": "",
        "company": "",
        "location": "",
        "experience": "",
        "education": "",
        "skills": [],
        "responsibilities": []
    }

    # Job Title

    first_line = lines[0]

    if "." in first_line:
        job["job_title"] = normalize_role(
            first_line.split(".", 1)[1].strip()
        )

    # Company + Location

    for line in lines:

        if line.startswith("Company:"):

            parts = line.split("|")

            job["company"] = (
                parts[0]
                .replace("Company:", "")
                .strip()
            )

            if len(parts) > 1:

                job["location"] = (
                    parts[1]
                    .replace("Location:", "")
                    .strip()
                )

        # Experience

        experience_match = re.search(
            r"\d+\+\s*years",
            line,
            re.IGNORECASE
        )

        if experience_match:
            job["experience"] = experience_match.group()

        # Education

        if "Bachelor" in line or "Master" in line:
            job["education"] = line

    # Responsibilities

    if "Responsibilities:" in job_text:

        responsibilities = (
            job_text
            .split("Responsibilities:")[1]
            .split("Requirements:")[0]
        )

        for item in responsibilities.split("-"):

            item = item.strip()

            if item:
                job["responsibilities"].append(item)

    # Skills

    skills = []

    keywords = [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Java",
        "JavaScript",
        "AWS",
        "Azure",
        "SEO",
        "Google Analytics",
        "CRM",
        "HRIS",
        "PMP"
    ]

    for keyword in keywords:

        if keyword.lower() in job_text.lower():

            skills.append(normalize_skill(keyword))

    job["skills"] = skills

    return job


def parse_job_descriptions(file_path):
    """
    Parse all job descriptions from a DOCX document.
    """

    text = read_docx(file_path)

    job_blocks = split_job_descriptions(text)

    parsed_jobs = []

    for block in job_blocks:
        parsed_jobs.append(
            extract_job_data(block)
        )

    return parsed_jobs