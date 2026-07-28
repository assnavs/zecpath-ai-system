"""
Education Normalizer

Normalizes education degree names into standard abbreviations.
"""

import json
from pathlib import Path


class EducationNormalizer:

    def __init__(self):
        dictionary_path = Path("data/education_dictionary.json")

        with open(dictionary_path, "r", encoding="utf-8") as file:
            self.degree_dictionary = json.load(file)

    def normalize(self, degree):

        if not degree:
            return ""

        degree = degree.strip()

        return self.degree_dictionary.get(degree, degree)