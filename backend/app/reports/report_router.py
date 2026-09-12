from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.service_container import assessment_service


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/{student_id}")
def get_student_report(student_id: str):

    return assessment_service.get_student_report(
        student_id
    )


@router.get("/{student_id}/export")
def export_student_report(student_id: str):

    pdf = assessment_service.export_student_report(
        student_id
    )

    if pdf is None:
        return {
            "success": False,
            "message": "Unable to generate report."
        }

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="SignSync_Report_{student_id}.pdf"'
        }
    )