from fastapi import APIRouter
from app.admin.admin_monitoring_service import (
    AdminMonitoringService
)
from app.services.admin.admin_analytics_service import (
    AdminAnalyticsService
)
from fastapi.responses import StreamingResponse

from app.services.admin.admin_report_export_service import (
    AdminReportExportService
)
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

analytics_service = AdminAnalyticsService()
export_service = (
    AdminReportExportService()
)
monitoring_service = (
    AdminMonitoringService()
)
# =====================================================
# PLATFORM ANALYTICS
# =====================================================

@router.get("/analytics")
def get_admin_analytics():

    return {
        "success": True,
        "analytics":
            analytics_service.get_dashboard_analytics()
    }


# =====================================================
# PLATFORM STATISTICS ONLY
# =====================================================
@router.get("/system-monitoring")
def get_system_monitoring():

    return {

        "success": True,

        "metrics":
            monitoring_service.get_system_metrics()
    }
@router.get("/statistics")
def get_platform_statistics():

    return {
        "success": True,
        "statistics":
            analytics_service.get_platform_statistics()
    }


# =====================================================
# USER GROWTH
# =====================================================

@router.get("/user-growth")
def get_user_growth():

    return {
        "success": True,
        "data":
            analytics_service.get_user_growth()
    }


# =====================================================
# ACCURACY TRENDS
# =====================================================

@router.get("/accuracy-trends")
def get_accuracy_trends():

    return {
        "success": True,
        "data":
            analytics_service.get_accuracy_trends()
    }


# =====================================================
# ASSESSMENT ACTIVITY
# =====================================================

@router.get("/assessment-activity")
def get_assessment_activity():

    return {
        "success": True,
        "data":
            analytics_service.get_assessment_activity()
    }
@router.get("/export/excel")
def export_excel_report():

    file_stream = (
        export_service.generate_excel_report()
    )

    return StreamingResponse(

        file_stream,

        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={
            "Content-Disposition":
            "attachment; filename=SignSync_Report.xlsx"
        }
    )