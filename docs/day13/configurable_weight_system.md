# Configurable Weight System

## Overview

The Configurable Weight System is a core component of the ATS Scoring Framework that enables flexible candidate evaluation based on different job roles. Instead of using a fixed scoring formula for every position, the system allows each job role to define its own scoring priorities through a JSON-based configuration file.

This approach improves the adaptability of the ATS by ensuring that different positions are evaluated according to the competencies that are most important for that role.

---

# Objective

The objective of the Configurable Weight System is to provide a flexible and maintainable mechanism for assigning different importance levels to evaluation parameters without modifying the application source code.

The system should:

- Support multiple job roles.
- Allow role-specific scoring priorities.
- Eliminate hard-coded weight values.
- Simplify future modifications.
- Improve maintainability and scalability.

---

# Why Dynamic Weight Configuration?

Different job roles require different evaluation priorities.

For example:

- A Data Scientist requires strong analytical and machine learning skills.
- A Frontend Developer requires expertise in UI technologies and frameworks.
- A Backend Developer requires stronger emphasis on server-side development and system architecture.

Using a single scoring formula for every role would not produce accurate candidate evaluations. Therefore, the ATS uses a configurable weight system that can assign different weights based on the selected job role.

---

# Configuration File

The weight configuration is stored in a JSON file.

File Location:

```
data/ats_weight_configuration.json
```

The JSON file contains separate weight configurations for different job roles.

Example:

```json
{
    "Data Scientist": {
        "skill_match": 0.40,
        "experience_relevance": 0.20,
        "education_alignment": 0.10,
        "semantic_similarity": 0.30
    },
    "Frontend Developer": {
        "skill_match": 0.35,
        "experience_relevance": 0.25,
        "education_alignment": 0.10,
        "semantic_similarity": 0.30
    },
    "Backend Developer": {
        "skill_match": 0.35,
        "experience_relevance": 0.30,
        "education_alignment": 0.10,
        "semantic_similarity": 0.25
    }
}
```

---

# Weight Parameters

The configuration defines four primary evaluation parameters.

## Skill Match

Measures how well the candidate's technical skills align with the required job skills.

---

## Experience Relevance

Measures the relevance of the candidate's professional experience to the selected job role.

---

## Education Alignment

Measures whether the candidate's educational qualifications satisfy the expected academic requirements.

---

## Semantic Similarity

Measures the contextual similarity between the resume and the job description using semantic embeddings.

---

# Working Process

The Configurable Weight System follows these steps:

1. The ATS receives the selected job role.
2. The system loads the JSON configuration file.
3. The corresponding weight configuration is retrieved.
4. The ATS applies the role-specific weights during score calculation.
5. The final ATS score is generated.

This process allows the same scoring engine to evaluate multiple job roles without changing the application logic.

---

# Advantages

The Configurable Weight System offers several benefits:

- Role-specific candidate evaluation.
- Easy configuration through JSON.
- No code modification required for weight changes.
- Better maintainability.
- Improved scalability.
- Supports future job roles.
- Reduces hard-coded values.

---

# Future Enhancements

The current implementation can be extended by supporting additional features such as:

- Industry-specific weight configurations.
- Company-specific scoring preferences.
- Automatic weight optimization using machine learning.
- Administrative interface for updating weights.
- Database-based configuration management.

---

# Conclusion

The Configurable Weight System provides a flexible and scalable mechanism for assigning role-specific scoring priorities within the ATS Resume Screening System. By separating weight definitions from the application logic, the system becomes easier to maintain, extend, and customize for different recruitment scenarios. This approach improves the fairness and accuracy of candidate evaluation while supporting future enhancements with minimal development effort.