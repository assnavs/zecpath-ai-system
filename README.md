# Zecpath AI System

## Overview

This project provides the initial development environment and modular architecture for an AI-powered recruitment platform. It follows a microservices-inspired structure, making the system scalable, maintainable, and easy to extend.

## Project Structure

```
zecpath-ai-system/
│
├── ats_engine/        # ATS scoring module
├── data/              # Data storage
├── docs/              # Project documentation
├── interview_ai/      # Interview intelligence
├── logs/              # Application logs
├── parsers/           # Resume parser
├── scoring/           # Final scoring engine
├── screening_ai/      # Candidate screening
├── tests/             # Unit tests
├── utils/             # Utility modules
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies Used

- Python
- FastAPI
- Flask
- Pandas
- NumPy
- Scikit-learn
- Git
- Visual Studio Code

## Installation

```bash
git clone <repository-url>

cd zecpath-ai-system

python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Author

Assna V S

Data Science Engineer (Intern)

Zecser Business LLP