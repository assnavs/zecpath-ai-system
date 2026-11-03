# Day 46 — Technical Question Hierarchy Model

## 1. Objective

The objective is to organize technical interview questions according to job role, relevant skills, experience level, and question difficulty.

## 2. Question Classification

Questions are organized into three experience categories.

| Experience Category | Experience Range | Configured Difficulty |
|---|---|---|
| Entry | 0–2 years | Basic |
| Intermediate | 3–4.99 years | Intermediate |
| Advanced | 5+ years | Advanced |

## 3. Role-wise Skill Mapping

### 3.1 MERN Developer

- MongoDB
- Express.js
- React
- Node.js
- JavaScript

### 3.2 Java Developer

- Java
- Object-Oriented Programming
- Spring Boot
- SQL
- REST APIs

### 3.3 DevOps Engineer

- Linux
- Docker
- Kubernetes
- CI/CD
- AWS
- Monitoring

## 4. Question Categories

| Category | Purpose |
|---|---|
| Experience-based | Understand previous technical work and practical experience |
| Conceptual | Evaluate understanding of technical concepts |
| Scenario-based | Evaluate approaches to practical technical situations |

## 5. Sample Question Hierarchy

### MERN Developer

| Level | Skill | Difficulty | Sample Question |
|---|---|---|---|
| Entry | JavaScript | Basic | Explain the difference between var, let and const. |
| Intermediate | Node.js | Intermediate | Describe how you built and structured a REST API using Node.js. |
| Advanced | Node.js | Advanced | Explain how Node.js handles concurrency and asynchronous workloads. |

### Java Developer

| Level | Skill | Difficulty | Sample Question |
|---|---|---|---|
| Entry | Java | Basic | Explain the main features of Java. |
| Intermediate | Spring Boot | Intermediate | Explain dependency injection in Spring Boot. |
| Advanced | Java | Advanced | Explain Java concurrency and thread synchronization. |

### DevOps Engineer

| Level | Skill | Difficulty | Sample Question |
|---|---|---|---|
| Entry | Docker | Basic | What is a Docker image and how is it different from a container? |
| Intermediate | Kubernetes | Intermediate | Explain the role of Pods and Deployments in Kubernetes. |
| Advanced | Kubernetes | Advanced | Design a highly available Kubernetes deployment. |

## 6. Question Selection Logic

The Technical Interview Engine:

1. Receives the technical role and experience in years.
2. Validates the role and experience input.
3. Determines the experience classification.
4. Loads the corresponding role-specific question set.
5. Returns the selected questions with skill and difficulty information.

## 7. Limitations

The current configuration provides initial sample questions for three roles.

The system selects questions using experience classification. It does not yet adapt the next question's difficulty dynamically according to the candidate's previous answer.

The question bank can be expanded through configuration updates.
