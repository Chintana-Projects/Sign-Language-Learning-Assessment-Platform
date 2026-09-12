from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.content.lesson_service import LessonService
from app.schemas.lesson_schema import LessonCreate

router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)


lesson_service = LessonService()


# ==========================================================
# GET ALL LESSONS
# ==========================================================

@router.get("/")
def get_lessons(
    db: Session = Depends(get_db)
):
    """
    Return all available lessons.
    """

    return lesson_service.get_all_lessons(db)


# ==========================================================
# GET LESSON BY ID
# ==========================================================

@router.get("/{lesson_id}")
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Return complete details for a selected lesson.
    """

    lesson = lesson_service.get_lesson_by_id(
        db,
        lesson_id
    )

    if lesson is None:

        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson

# ==========================================================
# UPDATE LESSON
# ==========================================================

@router.put("/{lesson_id}")
def update_lesson(
    lesson_id: int,
    title: str,
    description: str,
    category: str,
    db: Session = Depends(get_db)
):
    """
    Update lesson content.
    """

    lesson = lesson_service.update_lesson(
        db,
        lesson_id,
        title,
        description,
        category
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson

# ==========================================================
# UPDATE LESSON STATUS
# ==========================================================

@router.patch("/{lesson_id}/status")
def update_lesson_status(
    lesson_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):
    """
    Activate or deactivate a lesson.
    """

    lesson = lesson_service.update_lesson_status(
        db,
        lesson_id,
        is_active
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return lesson   

# ==========================================================
# CREATE LESSON
# ==========================================================

@router.post("/")
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db)
):

    return lesson_service.create_lesson(
        db,
        lesson
    )

@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):

    deleted = lesson_service.delete_lesson(
        db,
        lesson_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    return {
        "success": True,
        "message": "Lesson deleted"
    }