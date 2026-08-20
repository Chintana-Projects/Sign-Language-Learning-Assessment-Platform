from fastapi import APIRouter, HTTPException

from app.core.container import instructor_dashboard_service


router = APIRouter(
    prefix="/instructor",
    tags=["Instructor Dashboard"]
)


# =====================================================
# Instructor Dashboard
# =====================================================

@router.get("/dashboard")
def get_dashboard():

    return instructor_dashboard_service.get_dashboard()


# =====================================================
# Individual Student Details
# =====================================================

@router.get("/students/{student_id}")
def get_student_details(student_id: str):

    try:

        return instructor_dashboard_service.get_student_details(
            student_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Unable to load student details."
        )