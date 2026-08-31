from fastapi import APIRouter

from app.core.service_container import assessment_service


# ============================================================
# REPORT ROUTER
# ============================================================

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# ============================================================
# GET STUDENT REPORT
# ============================================================

@router.get("/{student_id}")
def get_student_report(student_id: str):

    return assessment_service.get_student_report(
        student_id
    )