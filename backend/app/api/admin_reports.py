from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.admin.admin_report_export_service import (
    AdminReportExportService
)

router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"]
)

export_service = (
    AdminReportExportService()
)


@router.get("/export")
def export_report():

    excel_file = (
        export_service
        .generate_excel_report()
    )

    return StreamingResponse(
        excel_file,
        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            "attachment; filename=SignSync_Admin_Report.xlsx"
        }
    )