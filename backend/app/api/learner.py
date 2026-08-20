from fastapi import APIRouter

from app.core.container import assessment_service

router = APIRouter(
    prefix="/learner",
    tags=["Learner"]
)


# IMPORTANT:
# Use the SAME LearnerProfileService instance
# that AssessmentService uses during practice.
profile_service = assessment_service.learner_profile_service


@router.get("/profile/{student_id}")
def learner_profile(
    student_id: str
):

    return {

        "success": True,

        "profile":
            profile_service.generate_profile(
                student_id
            )

    }