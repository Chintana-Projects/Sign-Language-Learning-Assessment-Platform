from fastapi import APIRouter

from app.core.container import instructor_dashboard_service

router = APIRouter(
    prefix="/instructor",
    tags=["Instructor"]
)


# =====================================================
# Instructor Dashboard
# =====================================================

@router.get("/dashboard")
def get_dashboard():
    """
    Returns instructor dashboard analytics.
    """

    return instructor_dashboard_service.get_dashboard()