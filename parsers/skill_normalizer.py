"""
Skill Normalizer

This module standardizes skill names and job role variations.
"""


SKILL_SYNONYMS = {
    # Excel
    "MS Excel": "Excel",
    "Microsoft Excel": "Excel",
    "Excel": "Excel",

    # SQL
    "SQL Server": "SQL",
    "MySQL": "SQL",
    "PostgreSQL": "SQL",
    "SQL": "SQL",

    # Python
    "Py": "Python",
    "Python3": "Python",
    "Python": "Python",

    # JavaScript
    "JS": "JavaScript",
    "Javascript": "JavaScript",
    "JavaScript": "JavaScript",

    # Power BI
    "PowerBI": "Power BI",
    "Power BI": "Power BI",

    # Tableau
    "Tableau Desktop": "Tableau",
    "Tableau": "Tableau"
}


ROLE_SYNONYMS = {
    "Data Analyst": "Data Analyst",
    "Business Data Analyst": "Data Analyst",

    "Software Engineer": "Software Engineer",
    "Software Developer": "Software Engineer",

    "Web Developer": "Web Developer",
    "Frontend Developer": "Web Developer",
    "Backend Developer": "Web Developer",

    "HR Executive": "HR Coordinator",
    "HR Coordinator": "HR Coordinator",

    "Digital Marketing Executive": "Digital Marketing Manager",
    "Digital Marketing Manager": "Digital Marketing Manager",

    "Graduate Trainee": "Graduate Trainee",
    "Business Associate": "Graduate Trainee",

    "Accountant": "Senior Accountant",
    "Senior Accountant": "Senior Accountant"
}


def normalize_skill(skill):
    """
    Normalize a skill name.
    """
    skill = skill.strip()
    return SKILL_SYNONYMS.get(skill, skill)


def normalize_role(role):
    """
    Normalize a job role.
    """
    role = role.strip()
    return ROLE_SYNONYMS.get(role, role)