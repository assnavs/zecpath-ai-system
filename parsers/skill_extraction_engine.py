"""
Skill Extraction Engine

Extracts technical and non-technical skills from resume text.
Supports:
- Skill dictionary lookup
- Synonyms
- Skill stacks
- Spelling variations
- Confidence scoring
- Deduplication
- Structured JSON output
"""

import json
import re
from pathlib import Path

from parsers.skill_normalizer import normalize_skill
from utils.logger import logger


class SkillExtractionEngine:
    """
    Skill Extraction Engine
    """

    def __init__(self):
        dictionary_path = Path("data/master_skill_dictionary.json")

        with open(dictionary_path, "r", encoding="utf-8") as file:
            self.skill_dictionary = json.load(file)

    def _find_skills(self, text, category_name):
        """
        Find skills belonging to a specific category.
        """

        found_skills = []

        category = self.skill_dictionary.get(category_name, {})

        for skill_name, details in category.items():

            search_terms = []

            search_terms.append(skill_name)

            search_terms.extend(details.get("synonyms", []))

            search_terms.extend(details.get("variations", []))

            confidence = 0.0

            matched = False

            for term in search_terms:

                pattern = r"\b" + re.escape(term.lower()) + r"\b"

                if re.search(pattern, text):

                    matched = True

                    if term == skill_name:
                        confidence = max(confidence, 1.00)

                    elif term in details.get("synonyms", []):
                        confidence = max(confidence, 0.95)

                    else:
                        confidence = max(confidence, 0.90)

            if matched:

                normalized = normalize_skill(skill_name)

                found_skills.append(
                    {
                        "skill": normalized,
                        "category": details.get("category", category_name),
                        "confidence": round(confidence, 2)
                    }
                )

        return found_skills

    def _expand_skill_stacks(self, extracted_skills, resume_text):
        """
        Detect and expand skill stacks like MERN, MEAN.
        """

        existing = {item["skill"] for item in extracted_skills}

        stacks = self.skill_dictionary.get("skill_stacks", {})

        resume_text = resume_text.lower()

        for stack_name, technologies in stacks.items():

            if stack_name.lower() in resume_text:

                for tech in technologies:

                    tech = normalize_skill(tech)

                    if tech not in existing:

                        extracted_skills.append(
                            {
                                "skill": tech,
                                "category": "Stack Component",
                                "confidence": 0.85
                            }
                        )

                        existing.add(tech)

        return extracted_skills
    
    def _remove_duplicates(self, skills):
        """
        Remove duplicate skills.
        """

        unique = {}

        for skill in skills:

            name = skill["skill"]

            if name not in unique:

                unique[name] = skill

            else:

                if skill["confidence"] > unique[name]["confidence"]:

                    unique[name] = skill

        return list(unique.values())

    def extract(self, resume_text):
        """
        Extract all skills from resume.
        """

        logger.info("Starting skill extraction...")

        text = resume_text.lower()

        technical = self._find_skills(text, "technical")

        business = self._find_skills(text, "business")

        creative = self._find_skills(text, "creative")

        skills = technical + business + creative

        skills = self._expand_skill_stacks(skills, text)

        skills = self._remove_duplicates(skills)

        logger.info("Skill extraction completed.")

        return {
            "total_skills": len(skills),
            "skills": sorted(
                skills,
                key=lambda x: x["confidence"],
                reverse=True
            )
        }


if __name__ == "__main__":

    sample_resume = """
    Experienced Data Analyst with Python, SQL Server,
    PowerBI, Tableau Desktop, Excel,
    Communication and Leadership skills.

    Worked on MERN projects.
    """

    engine = SkillExtractionEngine()

    result = engine.extract(sample_resume)

    print(json.dumps(result, indent=4))