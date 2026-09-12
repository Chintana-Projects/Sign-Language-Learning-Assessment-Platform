from fastapi import APIRouter, HTTPException

from app.core.container import assessment_service
from fastapi.responses import StreamingResponse
router = APIRouter(
    prefix="/assessment",
    tags=["Assessment"]
)


# =========================================================
# CHECK ASSESSMENT UNLOCK STATUS
# =========================================================

@router.get("/status/{student_id}")
def get_assessment_status(
    student_id: str
):
    """
    Check whether the student has completed
    all A-Z alphabet lessons and can start
    the final assessment.
    """

    try:

        profile = (
            assessment_service
            .learner_profile_service
            .get_profile(
                student_id
            )
        )

        if profile is None:

            return {
                "success": True,
                "student_id": student_id,
                "unlocked": False,
                "completed_letters": [],
                "completed_count": 0,
                "remaining_letters": [
                    chr(i)
                    for i in range(
                        ord("A"),
                        ord("Z") + 1
                    )
                ],
                "remaining_count": 26
            }


        completed_letters = profile.get(
            "completed_letters",
            []
        )


        completed_letters = [
            str(letter).upper()
            for letter in completed_letters
        ]


        all_letters = [
            chr(i)
            for i in range(
                ord("A"),
                ord("Z") + 1
            )
        ]


        remaining_letters = [

            letter

            for letter in all_letters

            if letter not in completed_letters

        ]


        unlocked = (
            len(remaining_letters) == 0
        )


        return {

            "success": True,

            "student_id":
                student_id,

            "unlocked":
                unlocked,

            "completed_letters":
                completed_letters,

            "completed_count":
                len(
                    completed_letters
                ),

            "remaining_letters":
                remaining_letters,

            "remaining_count":
                len(
                    remaining_letters
                )

        }


    except Exception as e:

        print(
            "Assessment status error:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =========================================================
# START FINAL ASSESSMENT
# =========================================================

@router.post("/start/{student_id}")

@router.post("/start/{student_id}")
def start_assessment(student_id: str):

    all_letters = [
        chr(i)
        for i in range(
            ord("A"),
            ord("Z") + 1
        )
    ]

    return {

        "success": True,

        "unlocked": True,

        "student_id": student_id,

        "message": "Assessment unlocked.",

        "assessment": {

            "status": "ready",

            "total_letters": 26,

            "letters": all_letters

        }

    }


# =========================================================
# GET ASSESSMENT HISTORY FOR STUDENT
# =========================================================

@router.get("/history/{student_id}")
def get_assessment_history(
    student_id: str
):
    """
    Return all assessment attempts
    belonging to a student.
    """

    try:

        result = (
            assessment_service
            .get_student_assessments(
                student_id
            )
        )


        return {

            "success": True,

            "student_id":
                student_id,

            "assessments":
                result

        }


    except Exception as e:

        print(
            "Assessment history error:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =========================================================
# GET SINGLE ASSESSMENT
# =========================================================

@router.get("/{assessment_id}")
def get_assessment(
    assessment_id: str
):
    """
    Return a single assessment record.
    """

    try:

        history = (
            assessment_service
            .get_assessment_history()
        )


        if history is None:

            raise HTTPException(

                status_code=404,

                detail="Assessment history not found"

            )


        for assessment in history:

            if str(
                assessment.get(
                    "assessment_id"
                )
            ) == str(
                assessment_id
            ):

                return {

                    "success": True,

                    "assessment":
                        assessment

                }


        raise HTTPException(

            status_code=404,

            detail="Assessment not found"

        )


    except HTTPException:

        raise


    except Exception as e:

        print(
            "Get assessment error:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
    # =========================================================
# GET STUDENT REPORT
# =========================================================

@router.get("/report/{student_id}")
def get_student_report(
    student_id: str
):
    """
    Return a simple learning report
    for a student.
    """

    try:

        result = (
            assessment_service
            .get_student_report(
                student_id
            )
        )

        return result

    except Exception as e:

        print(
            "Student report error:",
            e
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )
@router.get("/report/{student_id}/export")
def export_student_report(student_id: str):

    try:

        pdf_buffer = (
            assessment_service.export_student_report(
                student_id
            )
        )

        if pdf_buffer is None:

            raise HTTPException(
                status_code=404,
                detail="Report not found"
            )

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f'attachment; filename="SignSync_Report_{student_id}.pdf"'
            }
        )

    except Exception as e:

        print("Export report error:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )