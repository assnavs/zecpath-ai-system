"""
Semantic Matching Engine

Optimized semantic similarity computation.

Day 18 improvements:
- Shared SentenceTransformer model
- Reduced repeated model loading
- Batch embedding generation
- Normalized embeddings
- Direct dot-product similarity
- Reduced unnecessary memory allocation
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from utils.logger import logger


class SemanticMatchingEngine:
    """
    Compute semantic similarity between resume
    sections and job-description sections.

    The embedding model is shared between engine
    instances to avoid repeated expensive loading.
    """

    _model = None

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        logger.info(
            "Initializing Semantic Matching Engine..."
        )

        # Load the model only once and reuse it
        # across multiple engine instances.
        if SemanticMatchingEngine._model is None:

            logger.info(
                "Loading semantic embedding model..."
            )

            SemanticMatchingEngine._model = (
                SentenceTransformer(
                    self.MODEL_NAME
                )
            )

        self.model = (
            SemanticMatchingEngine._model
        )

        threshold_path = (
            Path(__file__)
            .resolve()
            .parent
            .parent
            / "data"
            / "semantic_similarity_thresholds.json"
        )

        with open(
            threshold_path,
            "r",
            encoding="utf-8",
        ) as file:

            self.thresholds = json.load(file)

    def generate_embedding(
        self,
        text,
    ):
        """
        Generate a normalized embedding
        for a single text value.
        """

        safe_text = (
            str(text)
            if text
            else ""
        )

        return self.model.encode(
            safe_text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def calculate_similarity(
        self,
        resume_text,
        jd_text,
    ):
        """
        Compute semantic similarity between
        resume text and job-description text.

        Both texts are encoded together in
        a single batch operation.
        """

        texts = [
            str(resume_text or ""),
            str(jd_text or ""),
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        similarity = np.dot(
            embeddings[0],
            embeddings[1],
        )

        return round(
            float(similarity) * 100,
            2,
        )

    def classify_match(
        self,
        score,
    ):
        """
        Classify similarity score using
        configured thresholds.
        """

        score = float(score)

        for value in self.thresholds.values():

            if (
                value["min_score"]
                <= score
                <= value["max_score"]
            ):
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
        Calculate semantic similarity across
        skills, experience, and projects.

        All six text values are encoded in one
        batch operation for improved performance.
        """

        texts = [
            str(resume_skills or ""),
            str(jd_skills or ""),
            str(resume_experience or ""),
            str(jd_experience or ""),
            str(resume_projects or ""),
            str(jd_projects or ""),
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        skills_score = float(
            np.dot(
                embeddings[0],
                embeddings[1],
            )
            * 100
        )

        experience_score = float(
            np.dot(
                embeddings[2],
                embeddings[3],
            )
            * 100
        )

        projects_score = float(
            np.dot(
                embeddings[4],
                embeddings[5],
            )
            * 100
        )

        overall_score = (
            skills_score
            + experience_score
            + projects_score
        ) / 3

        result = {
            "skills_similarity": round(
                float(skills_score),
                2,
            ),
            "experience_similarity": round(
                float(experience_score),
                2,
            ),
            "projects_similarity": round(
                float(projects_score),
                2,
            ),
            "overall_similarity": round(
                float(overall_score),
                2,
            ),
            "match_level": self.classify_match(
                float(overall_score)
            ),
        }

        logger.info(
            "Semantic similarity calculated: %.2f%%",
            overall_score,
        )

        return result