from fastapi import APIRouter, HTTPException, Depends

from app.schemas.landmarks import LandmarkRequest
from app.review.practice_review import PracticeReview
from sqlalchemy.orm import Session

from app.core.container import assessment_service

from app.database.database import get_db
router = APIRouter(
    prefix="/practice",
    tags=["Practice"]
)


# =========================================================
# START PRACTICE
# =========================================================

@router.post("/start/{lesson_id}/{student_id}")
def start_practice(
    lesson_id: int,
    student_id: str,
    db: Session = Depends(get_db)
):
    print("\n========== START PRACTICE ==========")
    print("Requested lesson :", lesson_id)
    print("Student :", student_id)

    result = assessment_service.start_practice(
        db=db,
        lesson_id=lesson_id,
        student_id=student_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return result


# =========================================================
# LESSON BY LETTER
# =========================================================
@router.get("/lesson/{letter}")
def get_lesson_by_letter(
    letter: str,
    db: Session = Depends(get_db)
):
    lesson = (
        assessment_service
        .lesson_service
        .get_lesson_by_letter(
            db,
            letter.upper()
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return {
        "success": True,
        "lesson": lesson
    }


# =========================================================
# FRAME PROCESSING
# =========================================================

@router.post("/{session_id}/frame")
def process_frame(
    session_id: str,
    request: LandmarkRequest
):
    try:
        result = assessment_service.process_frame(
            session_id=session_id,
            landmarks=request.landmarks,
            hand_count=request.hand_count,
            person_count=request.person_count,
            body_visible=request.body_visible
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "success": result.get(
            "success",
            True
        ),
        "message": "Frame processed",
        "prediction": result.get(
            "prediction",
            "UNKNOWN"
        ),
        "confidence": result.get(
            "confidence",
            0
        ),
        "top_predictions": result.get(
            "top_predictions",
            []
        ),
        "stable_prediction": result.get(
            "stable_prediction",
            {}
        ),
        "buffer_size": result.get(
            "buffer_size",
            0
        ),
        "buffer_full": result.get(
            "buffer_full",
            False
        ),
        "motion_metrics": result.get(
            "motion_metrics",
            {}
        ),
        "performance": result.get(
            "performance",
            {}
        ),
        "validation": result.get(
            "validation",
            {}
        )
    }


# =========================================================
# RECORD FINAL ATTEMPT
# =========================================================

@router.post("/{session_id}/attempt")
def record_attempt(
    session_id: str,
    request: LandmarkRequest,
    db: Session = Depends(get_db)
):
    print("\n========== ATTEMPT DEBUG ==========")
    print("Requested Session ID:", session_id)

    print(
        "Available Sessions:",
        list(
            assessment_service
            .session_service
            .sessions
            .keys()
        )
    )

    try:
        result = assessment_service.record_attempt(
            db=db,
            session_id=session_id,
            landmarks=request.landmarks,
            stable_prediction=request.stable_prediction,
            motion_metrics=request.motion_metrics
        )
    except ValueError as e:
        print("VALUE ERROR:", str(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        print("RECORD ATTEMPT ERROR:", str(e))

        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    print("\n========== ATTEMPT RESULT ==========")
    print(result)

    return {
        "success": result.get(
            "success",
            True
        ),
        "message": result.get(
            "message",
            ""
        ),
        "assessment": result.get(
            "assessment",
            {}
        ),
        "feedback": result.get(
            "feedback",
            {}
        ),
        "sign_score": result.get(
            "sign_score",
            {}
        ),
        "session": result.get(
            "session",
            {}
        ),
        "profile": result.get(
            "profile",
            {}
        ),
        "next_practice": result.get(
            "next_practice"
        )
    }


# =========================================================
# MOVE NEXT LETTER
# =========================================================

@router.post("/{session_id}/next")
def next_letter(
    session_id: str
):
    session = (
        assessment_service
        .session_service
        .get_session(
            session_id
        )
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if session.get("next_letter") is None:
        return {
            "success": False,
            "message": "Complete current letter attempt first",
            "current_letter": session.get(
                "current_letter"
            ),
            "next_letter": None,
            "session": session
        }

    updated_session = (
        assessment_service
        .session_service
        .move_to_next_letter(
            session_id
        )
    )

    if updated_session is None:
        raise HTTPException(
            status_code=404,
            detail="Unable to move next"
        )

    return {
        "success": True,
        "message": "Moved to next letter",
        "current_letter": updated_session.get(
            "current_letter"
        ),
        "next_letter": updated_session.get(
            "next_letter"
        ),
        "session": updated_session
    }


# =========================================================
# END PRACTICE
# =========================================================

@router.post("/{session_id}/end")
def end_practice(
    session_id: str
):
    session = assessment_service.end_practice(
        session_id
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return {
        "success": True,
        "message": "Practice session ended",
        "session": session
    }


# =========================================================
# REVIEW
# =========================================================

@router.get("/review/{session_id}")
def get_practice_review(
    session_id: str
):
    session = (
        assessment_service
        .session_service
        .get_session(
            session_id
        )
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    review = PracticeReview(
        session
    )

    print("\n========== REVIEW DEBUG ==========")
    print("Session ID:", session_id)
    print(
        "History Length:",
        len(
            session.get(
                "history",
                []
            )
        )
    )
    print(
        "Attempts:",
        session.get(
            "attempts"
        )
    )
    print(
        "Correct:",
        session.get(
            "correct_attempts"
        )
    )

    return {
        "success": True,
        "review": review.generate_review()
    }


# =========================================================
# HISTORY ROUTES
# KEEP BEFORE DYNAMIC ROUTES
# =========================================================

@router.get("/student/{student_id}/assessments")
def get_student_assessments(
    student_id: str
):
    return assessment_service.get_student_assessments(
        student_id
    )


@router.get("/{session_id}/assessments")
def get_session_assessments(
    session_id: str
):
    return assessment_service.get_session_assessments(
        session_id
    )


@router.get("/assessments")
def get_all_assessments():
    return assessment_service.get_assessment_history()


# =========================================================
# STUDENT ERROR ANALYSIS
# =========================================================

@router.get("/analytics/{student_id}")
def get_student_error_analysis(
    student_id: str
):
    return {
        "success": True,
        "analysis": assessment_service.get_error_analysis(
            student_id
        )
    }


# =========================================================
# PROFILE
# =========================================================

@router.get("/profile/{student_id}")
def get_profile(
    student_id: str
):
    return {
        "success": True,
        "profile": assessment_service.get_learner_profile(
            student_id
        )
    }


# =========================================================
# RECOMMENDATION QUEUE
# =========================================================

@router.get("/queue/{student_id}")
def get_learning_queue(
    student_id: str
):
    # Get learner profile
    profile = (
        assessment_service
        .get_learner_profile(
            student_id
        )
    )

    # Generate recommendations
    recommendations = (
        assessment_service
        .recommendation_engine
        .generate(
            profile
        )
    )

    return {
        "success": True,
        "student_id": student_id,
        "queue": recommendations
    }


# =========================================================
# DASHBOARD
# =========================================================

@router.get("/dashboard/{student_id}")
def get_dashboard(
    student_id: str
):
    return assessment_service.dashboard_service.get_dashboard(
        student_id
    )