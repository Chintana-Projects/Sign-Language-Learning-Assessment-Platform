from sqlalchemy import Column, Integer, String, Text, Boolean

from app.database.database import Base


class Lesson(Base):

    __tablename__ = "lessons"

    # =========================================
    # PRIMARY KEY
    # =========================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # =========================================
    # LESSON INFORMATION
    # =========================================

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    # Example:
    # A, B, C, Hello, Thank You, etc.

    category = Column(
        String(100),
        nullable=False
    )

    # =========================================
    # SIGN / LETTER
    # =========================================

    sign = Column(
        String(100),
        nullable=True
    )

    # =========================================
    # VIDEO / IMAGE
    # =========================================

    image_url = Column(
        String(500),
        nullable=True
    )

    video_url = Column(
        String(500),
        nullable=True
    )

    # =========================================
    # STATUS
    # =========================================

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )