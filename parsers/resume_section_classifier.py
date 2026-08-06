"""
Resume Section Classifier

Detects and classifies resume sections using
rule-based heading recognition.

Day 18 improvements:
- Header/Profile detection
- Reduced UNKNOWN classification
- Compiled normalization pattern
- Additional heading variants
- Cleaner section handling
"""

import re
import logging


logging.basicConfig(
    filename=(
        "logs/"
        "resume_section_classifier.log"
    ),
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
)


HEADING_CLEAN_PATTERN = re.compile(
    r"[^a-z0-9 ]"
)


class ResumeSectionClassifier:
    """
    Detect and classify resume sections.

    Content appearing before the first recognized
    resume section is treated as PROFILE instead
    of UNKNOWN.
    """

    SECTION_HEADINGS = {

        "profile": [
            "profile",
            "professional profile",
            "summary",
            "professional summary",
            "career summary",
            "objective",
            "career objective",
        ],

        "skills": [
            "skills",
            "technical skills",
            "core competencies",
            "key skills",
            "technical competencies",
        ],

        "work_experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "career history",
        ],

        "education": [
            "education",
            "academic qualifications",
            "qualification",
            "academic background",
            "educational qualifications",
        ],

        "certifications": [
            "certifications",
            "certificates",
            "licenses",
            "professional certifications",
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects",
            "professional projects",
        ],
    }

    def normalize_heading(
        self,
        text,
    ):
        """
        Normalize headings for comparison.
        """

        if not text:
            return ""

        text = str(text).lower()

        text = HEADING_CLEAN_PATTERN.sub(
            "",
            text,
        )

        return text.strip()

    def classify_sections(
        self,
        resume_text,
    ):
        """
        Identify resume sections based on headings.

        Resume content before the first recognized
        heading usually contains the candidate name,
        designation, contact header, or summary.

        This content is classified as PROFILE rather
        than UNKNOWN.
        """

        if not resume_text:
            return {}

        sections = {}

        # Day 18 improvement:
        # Resume header information should not
        # automatically become UNKNOWN.
        current_section = "profile"

        lines = str(
            resume_text
        ).splitlines()

        for line in lines:

            clean_line = (
                self.normalize_heading(
                    line
                )
            )

            if not clean_line:
                continue

            detected_section = None

            for (
                section,
                headings,
            ) in self.SECTION_HEADINGS.items():

                if clean_line in headings:

                    detected_section = section

                    break

            if detected_section:

                current_section = (
                    detected_section
                )

                sections.setdefault(
                    current_section,
                    [],
                )

                logging.info(
                    "Detected section: %s",
                    current_section,
                )

                continue

            sections.setdefault(
                current_section,
                [],
            ).append(
                line.strip()
            )

        return {
            section: "\n".join(
                content
            ).strip()

            for section, content
            in sections.items()

            if content
        }