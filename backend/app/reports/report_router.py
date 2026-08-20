from fastapi import APIRouter

from app.services.assessment_service import AssessmentService


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# Create one AssessmentService instance
assessment_service = AssessmentService()


@router.get("/{student_id}")
def get_student_report(student_id: str):

    return assessment_service.get_student_report(
        student_id
    )