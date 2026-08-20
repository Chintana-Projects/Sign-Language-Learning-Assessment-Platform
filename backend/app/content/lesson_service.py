# ==========================================================
# SignSync - Learning Content Service
# PostgreSQL-backed Learning Content
# ==========================================================

from sqlalchemy.orm import Session

from app.models.lesson_model import Lesson


class LessonService:

    # ------------------------------------------------------
    # Return all active lessons
    # ------------------------------------------------------

    def get_all_lessons(self, db: Session):
        return (
        db.query(Lesson)
        .order_by(Lesson.id)
        .all()
    )
    # ------------------------------------------------------
    # Return one lesson by ID
    # ------------------------------------------------------

    def get_lesson_by_id(
        self,
        db: Session,
        lesson_id: int
    ):

        return (
            db.query(Lesson)
            .filter(Lesson.id == lesson_id)
            .first()
        )

    # ------------------------------------------------------
    # Return one lesson by Letter
    # ------------------------------------------------------

    def get_lesson_by_letter(
        self,
        db: Session,
        letter: str
    ):

        return (
            db.query(Lesson)
            .filter(
                Lesson.sign == letter.upper(),
                Lesson.is_active == True
            )
            .first()
        )

    def update_lesson(
    self,
    db: Session,
    lesson_id: int,
    title: str,
    description: str,
    category: str
):
        lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )
        if lesson is None:
            return None
        lesson.title = title
        lesson.description = description
        lesson.category = category
        db.commit()
        db.refresh(lesson)
        return lesson


    def update_lesson_status(
    self,
    db: Session,
    lesson_id: int,
    is_active: bool
):
        lesson = (
        db.query(Lesson)
        .filter(Lesson.id == lesson_id)
        .first()
    )
        if lesson is None:
            return None
        lesson.is_active = is_active
        db.commit()
        db.refresh(lesson)
        return lesson