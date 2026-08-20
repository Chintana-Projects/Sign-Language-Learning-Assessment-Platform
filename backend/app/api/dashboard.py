from fastapi import APIRouter, Depends

from app.core.container import assessment_service
from app.auth.oauth2 import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def get_dashboard(
    current_user: dict = Depends(get_current_user)
):
    student_id = str(current_user["user_id"])

    return assessment_service.get_dashboard(
        student_id
    )