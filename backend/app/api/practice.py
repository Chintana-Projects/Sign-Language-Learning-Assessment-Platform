from fastapi import APIRouter, HTTPException, Depends
from app.auth.dependencies import get_current_user
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

@router.post("/start/{lesson_id}")
def start_practice(
    lesson_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    student_id = str(current_user["user_id"])

    # -----------------------------------------------------
    # Start the practice session
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # IMPORTANT:
    #
    # The selected lesson determines the expected letter.
    #
    # Lesson 1 -> A
    # Lesson 2 -> B
    # Lesson 3 -> C
    # ...
    # Lesson 4 -> D
    #
    # Do NOT let the recommendation/profile system replace
    # the letter the learner explicitly selected.
    # -----------------------------------------------------

    selected_letter = None

    if (
        isinstance(lesson_id, int)
        and 1 <= lesson_id <= 26
    ):
        selected_letter = chr(
            ord("A") + lesson_id - 1
        )

    # -----------------------------------------------------
    # Update the actual in-memory session
    # -----------------------------------------------------

    if selected_letter is not None:

        session = None

        # Try to get session ID from the response
        if isinstance(result, dict):

            session_id = result.get(
                "session_id"
            )

            if session_id is None:

                session_data = result.get(
                    "session"
                )

                if isinstance(
                    session_data,
                    dict
                ):
                    session_id = session_data.get(
                        "session_id"
                    )

            if session_id is not None:

                session = (
                    assessment_service
                    .session_service
                    .get_session(
                        session_id
                    )
                )

        # -------------------------------------------------
        # Force selected lesson as current/expected letter
        # -------------------------------------------------

        if session is not None:

            session["current_letter"] = (
                selected_letter
            )

            session["next_letter"] = (
                selected_letter
            )

            # The selected letter is the one being practiced.
            #
            # Do not mark it completed when starting.
            completed_letters = (
                session.get(
                    "completed_letters",
                    []
                )
            )

            if not isinstance(
                completed_letters,
                list
            ):
                completed_letters = []

            completed_letters = [
                str(letter).upper().strip()
                for letter in completed_letters
                if letter is not None
            ]

            completed_letters = list(
                dict.fromkeys(
                    completed_letters
                )
            )

            session["completed_letters"] = (
                completed_letters
            )

            # -------------------------------------------------
            # Remaining letters
            # -------------------------------------------------

            session["remaining_letters"] = [
                letter
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if letter not in completed_letters
            ]

            # -------------------------------------------------
            # Reset runtime prediction for the new letter
            # -------------------------------------------------

            session["latest_prediction"] = None

            session["latest_confidence"] = 0

            session["latest_stable_prediction"] = {
                "stable": False,
                "prediction": None,
                "confidence": 0,
                "stable_frames": 0,
                "unstable_frames": 0
            }

    # -----------------------------------------------------
    # Also update response data so frontend receives the
    # selected letter as the expected/current letter.
    # -----------------------------------------------------

    if isinstance(result, dict):

        result["current_letter"] = (
            selected_letter
            if selected_letter is not None
            else result.get("current_letter")
        )

        result["next_letter"] = (
            selected_letter
            if selected_letter is not None
            else result.get("next_letter")
        )

        session_data = result.get(
            "session"
        )

        if isinstance(
            session_data,
            dict
        ) and selected_letter is not None:

            session_data["current_letter"] = (
                selected_letter
            )

            session_data["next_letter"] = (
                selected_letter
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
    try:

        result = assessment_service.record_attempt(
            db=db,
            session_id=session_id,
            landmarks=request.landmarks,
            stable_prediction=request.stable_prediction,
            motion_metrics=request.motion_metrics
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

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

    # -----------------------------------------------------
    # Do not move until the current letter has been
    # successfully processed.
    # -----------------------------------------------------

    current_letter = session.get(
        "current_letter"
    )

    next_letter_value = session.get(
        "next_letter"
    )

    if next_letter_value is None:

        return {
            "success": False,
            "message": "Complete current letter attempt first",
            "current_letter": current_letter,
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
    profile = (
        assessment_service
        .get_learner_profile(
            student_id
        )
    )

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
    return (
        assessment_service
        .dashboard_service
        .get_dashboard(
            student_id
        )
    )