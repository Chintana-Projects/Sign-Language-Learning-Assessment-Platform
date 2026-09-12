# app/api/certification.py

from fastapi import APIRouter, HTTPException
from app.database.certificate_database import (
    CertificateDatabase
)
from app.core.container import (
    certification_service
)

from app.schemas.landmarks import (
    LandmarkRequest
)
certificate_db = CertificateDatabase()
router = APIRouter(
    prefix="/certification",
    tags=["Certification"]
)

# ==========================================================
# START CERTIFICATION
# ==========================================================

@router.post("/start/{student_id}")
def start_certification(student_id: str):

    try:

        result = certification_service.start_certification(
            student_id
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ==========================================================
# SUBMIT LETTER
# ==========================================================

@router.post(
    "/{certification_id}/submit"
)
def submit_letter(
    certification_id: str,
    predicted_letter: str,
    confidence: float = 1.0
):

    return (
        certification_service.submit_letter(
            certification_id=
                certification_id,

            predicted_letter=
                predicted_letter,

            confidence=
                confidence
        )
    )
@router.post(
    "/{certification_id}/frame"
)
def process_certification_frame(
    certification_id: str,
    request: LandmarkRequest
):

    session = certification_service.get_session(
        certification_id
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Certification session not found."
        )

    result = certification_service.process_frame(
        certification_id=certification_id,
        landmarks=request.landmarks,
        hand_count=request.hand_count,
        person_count=request.person_count,
        body_visible=request.body_visible
    )

    return result
@router.get("/status/{student_id}")
def get_certification_status(
    student_id: str
):

    try:

        profile = (
            certification_service
            .assessment_service
            .learner_profile_service
            .get_profile(student_id)
        )

        if not profile:

            return {
                "current_level": "Beginner",
                "lesson_progress": {
                    "percentage": 0
                },
                "certificate_id": None
            }

        return {

    "current_level":
        profile.get(
            "certification_level",
            "Beginner"
        ),

    "lesson_progress":
        profile.get(
            "lesson_progress",
            {
                "percentage": 0
            }
        ),

    "certificate_id":
        profile.get(
            "certificate_id"
        ),

    "certificates":
        profile.get(
            "certificates",
            []
        )
}

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ==========================================================
# GET RESULTS
# ==========================================================

@router.get(
    "/{certification_id}/results"
)
def get_results(
    certification_id: str
):

    return (
        certification_service.get_results(
            certification_id
        )
    )


# ==========================================================
# GET SESSION
# ==========================================================

@router.get(
    "/{certification_id}"
)
def get_session(
    certification_id: str
):

    session = (
        certification_service.get_session(
            certification_id
        )
    )

    if session is None:

        return {

            "success": False,

            "message":
                "Certification session not found."
        }

    return {

        "success": True,

        "session": session
    }
@router.get("/certificate/{certificate_id}")
def get_certificate(certificate_id: str):

    certificate = certificate_db.get_certificate(
        certificate_id
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    return {
        "success": True,
        "certificate": certificate
    }