import re
import logging

logging.basicConfig(
    filename="logs/resume_section_classifier.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class ResumeSectionClassifier:
    """
    Detects and classifies sections in a resume using rule-based heading matching.
    """

    SECTION_HEADINGS = {
        "skills": [
            "skills",
            "technical skills",
            "core competencies",
            "key skills"
        ],
        "work_experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history"
        ],
        "education": [
            "education",
            "academic qualifications",
            "qualification",
            "academic background"
        ],
        "certifications": [
            "certifications",
            "certificates",
            "licenses"
        ],
        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ]
    }

    def __init__(self):
        pass

    def normalize_heading(self, text):
        """
        Normalize headings for comparison.
        """
        text = text.lower()
        text = re.sub(r'[^a-z0-9 ]', '', text)
        return text.strip()

    def classify_sections(self, resume_text):
        """
        Identify resume sections based on headings.
        """

        sections = {}
        current_section = "unknown"

        lines = resume_text.splitlines()

        for line in lines:

            clean_line = self.normalize_heading(line)

            found = False

            for section, headings in self.SECTION_HEADINGS.items():

                if clean_line in headings:
                    current_section = section
                    sections[current_section] = []
                    found = True
                    logging.info(f"Detected section: {section}")
                    break

            if found:
                continue

            sections.setdefault(current_section, []).append(line)

        for key in sections:
            sections[key] = "\n".join(sections[key]).strip()

        return sections