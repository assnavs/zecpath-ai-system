"""
ATS REST API

Provides REST API endpoints for exposing ATS AI functionality
to backend systems.

Day 16 Features:
- Resume upload
- Resume parsing
- Candidate scoring
- Candidate shortlisting
- Asynchronous job status handling
- Standard response contracts
- Error handling
- Logging standards
"""

import uuid
from typing import Any, Dict, List

from fastapi import (
    BackgroundTasks,
    FastAPI,
    File,
    HTTPException,
    UploadFile,
)

from pydantic import BaseModel, Field

from scoring.ats_scoring_engine import ATSScoringEngine
from screening_ai.shortlisting import CandidateShortlistingEngine
from utils.logger import logger


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Zecpath ATS API",
    description=(
        "REST API interface for ATS resume processing, "
        "candidate scoring and shortlisting."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Temporary In-Memory Stores
# ---------------------------------------------------------

# These stores are suitable for Day 16 API design/testing.
# A production system should use persistent storage.

resume_store: Dict[str, Dict[str, Any]] = {}
job_store: Dict[str, Dict[str, Any]] = {}


# ---------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------

class ResumeParseRequest(BaseModel):
    """
    Request contract for resume parsing.
    """

    resume_text: str = Field(
        ...,
        min_length=1,
        description="Extracted candidate resume text",
    )


class CandidateScores(BaseModel):
    """
    Candidate evaluation scores used by the ATS scorer.
    """

    skill_match: float = Field(
        ...,
        ge=0,
        le=100,
    )

    experience_relevance: float = Field(
        ...,
        ge=0,
        le=100,
    )

    education_alignment: float = Field(
        ...,
        ge=0,
        le=100,
    )

    semantic_similarity: float = Field(
        ...,
        ge=0,
        le=100,
    )


class ScoringRequest(BaseModel):
    """
    Request contract for ATS candidate scoring.
    """

    job_role: str = Field(
        ...,
        min_length=1,
    )

    scores: CandidateScores


class CandidateInput(BaseModel):
    """
    Candidate contract used by the shortlisting API.
    """

    candidate_id: str = Field(
        ...,
        min_length=1,
    )

    name: str = Field(
        ...,
        min_length=1,
    )

    score: float = Field(
        ...,
        ge=0,
        le=100,
    )


class ShortlistingRequest(BaseModel):
    """
    Request contract for candidate shortlisting.
    """

    candidates: List[CandidateInput]


# ---------------------------------------------------------
# Standard Response Helpers
# ---------------------------------------------------------

def success_response(
    message: str,
    data: Any = None,
):
    """
    Create a standardized successful API response.
    """

    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    code: str,
    message: str,
):
    """
    Create a standardized error response.
    """

    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }


# ---------------------------------------------------------
# Async Job Handling
# ---------------------------------------------------------

def create_job(job_type: str):
    """
    Create a new asynchronous job record.
    """

    job_id = str(uuid.uuid4())

    job_store[job_id] = {
        "job_id": job_id,
        "job_type": job_type,
        "status": "QUEUED",
        "result": None,
        "error": None,
    }

    logger.info(
        "Created async job %s of type %s.",
        job_id,
        job_type,
    )

    return job_id


def process_resume_job(
    job_id: str,
    resume_id: str,
):
    """
    Demonstration background resume processing workflow.

    FastAPI BackgroundTasks is used for the Day 16
    asynchronous job handling design.
    """

    try:

        job_store[job_id]["status"] = "PROCESSING"

        logger.info(
            "Processing resume job %s.",
            job_id,
        )

        resume_record = resume_store.get(
            resume_id
        )

        if resume_record is None:
            raise ValueError(
                "Resume record could not be found."
            )

        # Integration point for the existing resume
        # extraction and parsing pipeline.
        #
        # Raw resume content is intentionally not logged.

        result = {
            "resume_id": resume_id,
            "filename": resume_record["filename"],
            "processing_status": "ready_for_parsing",
        }

        job_store[job_id]["result"] = result

        job_store[job_id]["status"] = (
            "COMPLETED"
        )

        logger.info(
            "Resume job %s completed.",
            job_id,
        )

    except Exception as exc:

        job_store[job_id]["status"] = "FAILED"

        job_store[job_id]["error"] = str(exc)

        logger.exception(
            "Resume job %s failed.",
            job_id,
        )


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------

@app.get("/api/v1/health")
def health_check():
    """
    Check whether the ATS API is operational.
    """

    logger.info(
        "ATS API health check requested."
    )

    return success_response(
        "ATS API is operational.",
        {
            "service": "Zecpath ATS API",
            "status": "healthy",
        },
    )


# ---------------------------------------------------------
# Resume Upload Endpoint
# ---------------------------------------------------------

@app.post("/api/v1/resumes/upload")
async def upload_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """
    Upload a candidate resume and create an
    asynchronous processing job.
    """

    logger.info(
        "Resume upload request received."
    )

    allowed_extensions = (
        ".pdf",
        ".docx",
    )

    filename = file.filename or ""

    if not filename.lower().endswith(
        allowed_extensions
    ):

        logger.warning(
            "Unsupported resume file type received."
        )

        raise HTTPException(
            status_code=400,
            detail=error_response(
                "INVALID_FILE_TYPE",
                (
                    "Only PDF and DOCX resume "
                    "files are supported."
                ),
            ),
        )

    file_content = await file.read()

    if not file_content:

        raise HTTPException(
            status_code=400,
            detail=error_response(
                "EMPTY_FILE",
                "Uploaded resume file is empty.",
            ),
        )

    resume_id = str(uuid.uuid4())

    resume_store[resume_id] = {
        "resume_id": resume_id,
        "filename": filename,
        "content": file_content,
    }

    job_id = create_job(
        "RESUME_PROCESSING"
    )

    background_tasks.add_task(
        process_resume_job,
        job_id,
        resume_id,
    )

    logger.info(
        "Resume accepted with ID %s.",
        resume_id,
    )

    return success_response(
        "Resume uploaded successfully.",
        {
            "resume_id": resume_id,
            "job_id": job_id,
            "status": "QUEUED",
        },
    )


# ---------------------------------------------------------
# Resume Parsing Endpoint
# ---------------------------------------------------------

@app.post("/api/v1/resumes/parse")
def parse_resume(
    request: ResumeParseRequest,
):
    """
    Resume parsing API contract.

    The existing parser pipeline can be connected
    to this endpoint during full integration.
    """

    logger.info(
        "Resume parsing request received."
    )

    cleaned_text = " ".join(
        request.resume_text.split()
    )

    if not cleaned_text:

        raise HTTPException(
            status_code=400,
            detail=error_response(
                "INVALID_REQUEST",
                "Resume text cannot be empty.",
            ),
        )

    parsed_result = {
        "text_length": len(cleaned_text),
        "status": "parsed",
        "integration": (
            "Existing resume parser pipeline "
            "can be connected here."
        ),
    }

    logger.info(
        "Resume parsing request completed."
    )

    return success_response(
        "Resume parsing completed.",
        parsed_result,
    )


# ---------------------------------------------------------
# ATS Scoring Endpoint
# ---------------------------------------------------------

@app.post("/api/v1/scoring")
def score_candidate(
    request: ScoringRequest,
):
    """
    Generate an ATS candidate score using the
    existing ATSScoringEngine.
    """

    logger.info(
        "Candidate scoring request received "
        "for role %s.",
        request.job_role,
    )

    try:

        engine = ATSScoringEngine()

        scores = request.scores.model_dump()

        # IMPORTANT:
        # ATSScoringEngine.calculate_score expects:
        #
        # job_role,
        # skill_match,
        # experience_relevance,
        # education_alignment,
        # semantic_similarity
        #
        # Therefore each score must be passed
        # individually instead of passing the
        # entire dictionary.

        result = engine.calculate_score(
            request.job_role,
            scores["skill_match"],
            scores["experience_relevance"],
            scores["education_alignment"],
            scores["semantic_similarity"],
        )

        logger.info(
            "Candidate scoring completed "
            "for role %s.",
            request.job_role,
        )

        return success_response(
            "Candidate scoring completed.",
            result,
        )

    except ValueError as exc:

        logger.warning(
            "Candidate scoring validation failed: %s",
            str(exc),
        )

        raise HTTPException(
            status_code=400,
            detail=error_response(
                "INVALID_JOB_ROLE",
                str(exc),
            ),
        )

    except Exception as exc:

        logger.exception(
            "Candidate scoring failed."
        )

        raise HTTPException(
            status_code=500,
            detail=error_response(
                "SCORING_ERROR",
                str(exc),
            ),
        )


# ---------------------------------------------------------
# Candidate Shortlisting Endpoint
# ---------------------------------------------------------

@app.post("/api/v1/shortlisting")
def shortlist_candidates(
    request: ShortlistingRequest,
):
    """
    Rank and shortlist candidates using the
    existing Day 14 shortlisting engine.
    """

    logger.info(
        "Candidate shortlisting request received."
    )

    try:

        engine = CandidateShortlistingEngine()

        candidates = [
            candidate.model_dump()
            for candidate in request.candidates
        ]

        result = engine.shortlist_candidates(
            candidates
        )

        logger.info(
            "Candidate shortlisting completed."
        )

        return success_response(
            "Candidate shortlisting completed.",
            result,
        )

    except Exception as exc:

        logger.exception(
            "Candidate shortlisting failed."
        )

        raise HTTPException(
            status_code=500,
            detail=error_response(
                "SHORTLISTING_ERROR",
                str(exc),
            ),
        )


# ---------------------------------------------------------
# Async Job Status Endpoint
# ---------------------------------------------------------

@app.get("/api/v1/jobs/{job_id}")
def get_job_status(
    job_id: str,
):
    """
    Retrieve the current status of an asynchronous
    processing job.
    """

    logger.info(
        "Job status requested for %s.",
        job_id,
    )

    job = job_store.get(
        job_id
    )

    if job is None:

        logger.warning(
            "Requested job %s was not found.",
            job_id,
        )

        raise HTTPException(
            status_code=404,
            detail=error_response(
                "RESOURCE_NOT_FOUND",
                "Requested job was not found.",
            ),
        )

    return success_response(
        "Job status retrieved.",
        job,
    )