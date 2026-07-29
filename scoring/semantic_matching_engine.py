import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from utils.logger import logger


class SemanticMatchingEngine:
    """
    Computes semantic similarity between resume sections and
    job description sections using sentence embeddings.
    """

    def __init__(self):
        logger.info("Initializing Semantic Matching Engine...")

        # Load pretrained embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Load similarity thresholds
        threshold_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "semantic_similarity_thresholds.json"
        )

        with open(threshold_path, "r", encoding="utf-8") as file:
            self.thresholds = json.load(file)

    def generate_embedding(self, text: str):
        """
        Generate embedding for a text.
        """
        if not text:
            return self.model.encode("")

        return self.model.encode(text)

    def calculate_similarity(self, resume_text: str, jd_text: str):
        """
        Compute cosine similarity between two text inputs.
        Returns percentage.
        """
        resume_embedding = self.generate_embedding(resume_text)
        jd_embedding = self.generate_embedding(jd_text)

        similarity = cosine_similarity(
            [resume_embedding],
            [jd_embedding]
        )[0][0]

        return float(round(similarity * 100, 2))

    def classify_match(self, score: float):
        """
        Classify similarity score using configured thresholds.
        """
        for value in self.thresholds.values():

            if value["min_score"] <= score <= value["max_score"]:
                return value["label"]

        return "Unknown"

    def calculate_overall_similarity(
        self,
        resume_skills,
        jd_skills,
        resume_experience,
        jd_experience,
        resume_projects,
        jd_projects,
    ):
        """
        Calculate semantic similarity across resume sections.
        """

        skills_score = self.calculate_similarity(
            resume_skills,
            jd_skills,
        )

        experience_score = self.calculate_similarity(
            resume_experience,
            jd_experience,
        )

        projects_score = self.calculate_similarity(
            resume_projects,
            jd_projects,
        )

        overall_score = round(
            (
                skills_score
                + experience_score
                + projects_score
            )
            / 3,
            2,
        )

        result = {
            "skills_similarity": round(float(skills_score), 2),
            "experience_similarity": round(float(experience_score), 2),
            "projects_similarity": round(float(projects_score), 2),
            "overall_similarity": round(float(overall_score), 2),
            "match_level": self.classify_match(float(overall_score)),
        }

        logger.info(
            f"Semantic similarity calculated: {overall_score}%"
        )

        return result