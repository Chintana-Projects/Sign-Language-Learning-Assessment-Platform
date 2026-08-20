from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


# =====================================================
# Shared Assessment Service
# =====================================================

from app.core.container import assessment_service



# =====================================================
# Analytics Modules
# =====================================================

from app.analytics.progress_analyzer import ProgressAnalyzer
from app.analytics.report_generator import ReportGenerator
from app.analytics.error_analysis_service import ErrorAnalysisService



# =====================================================
# Router
# =====================================================

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)




# =====================================================
# Error Analysis Service
# =====================================================






# =====================================================
# Student Progress Dashboard
# =====================================================

@router.get("/{student_id}")
def get_student_progress(
    student_id: str
):

    tracker = assessment_service.get_tracker(
        student_id
    )


    if tracker is None:

        raise HTTPException(

            status_code=404,

            detail="Student not found"

        )



    analyzer = ProgressAnalyzer(

        tracker.get_history()

    )



    return {

        "success": True,

        "progress":

            analyzer.summary()

    }







# =====================================================
# Error Analysis Module
# =====================================================

@router.get("/errors/{student_id}")
def get_error_analysis(
    student_id: str
):
    error_service = ErrorAnalysisService(
    assessment_service.assessment_history
)


    result = error_service.analyze_student(

        student_id

    )



    return {


        "success": True,


        "analysis":

            result

    }







# =====================================================
# Generate JSON Assessment Report
# =====================================================

@router.get("/{student_id}/report")
def generate_report(
    student_id: str
):


    tracker = assessment_service.get_tracker(

        student_id

    )



    if tracker is None:

        raise HTTPException(

            status_code=404,

            detail="Student not found"

        )



    analyzer = ProgressAnalyzer(

        tracker.get_history()

    )



    summary = analyzer.summary()



    report = ReportGenerator(

        analytics=summary,

        student_id=student_id

    )



    filename = report.save_json(

        f"{student_id}_assessment_report.json"

    )



    return {


        "success": True,


        "message":

            "Assessment report generated successfully.",


        "filename":

            filename,


        "report":

            report.generate_json()

    }








# =====================================================
# Generate PDF Assessment Report
# =====================================================

@router.get("/{student_id}/report/pdf")
def generate_pdf_report(
    student_id: str
):


    tracker = assessment_service.get_tracker(

        student_id

    )



    if tracker is None:

        raise HTTPException(

            status_code=404,

            detail="Student not found"

        )



    analyzer = ProgressAnalyzer(

        tracker.get_history()

    )



    summary = analyzer.summary()



    report = ReportGenerator(

        analytics=summary,

        student_id=student_id

    )



    filename = report.save_pdf(

        f"{student_id}_assessment_report.pdf"

    )



    return FileResponse(

        path=filename,

        media_type="application/pdf",

        filename=filename

    )