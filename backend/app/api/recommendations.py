from fastapi import APIRouter

from app.api.practice import assessment_service


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)



@router.get("/{student_id}")
def get_recommendations(
    student_id:str
):


    history = (
        assessment_service
        .assessment_history
        .get_student_history(
            student_id
        )
    )


    engine = (
        assessment_service
        .recommendation_engine
    )


    return {

        "success":True,

        "student_id":student_id,

        "recommendations":
        engine.generate(
            history
        )

    }