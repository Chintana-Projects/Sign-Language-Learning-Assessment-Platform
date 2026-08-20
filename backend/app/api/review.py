from fastapi import APIRouter, HTTPException

from app.api.practice import assessment_service
from app.review.practice_review import PracticeReview


router = APIRouter(
    prefix="/review",
    tags=["Practice Review"]
)


# ---------------------------------------------------------
# Get Practice Review
# ---------------------------------------------------------
@router.get("/{session_id}")
def get_review(session_id: str):
    # Get session through SessionService
    session = assessment_service.session_service.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    # Generate review
    review = PracticeReview(session)

    return {
        "success": True,
        "review": review.generate_review()
    }
