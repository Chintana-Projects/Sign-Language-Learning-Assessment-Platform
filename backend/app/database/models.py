from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Numeric
from sqlalchemy.sql import func

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String)

    email = Column(String, unique=True)

    password_hash = Column(String)

    role = Column(String)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


class LearnerProgress(Base):

    __tablename__ = "learner_progress"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    current_letter = Column(String(1))

    completed_letters = Column(String)

    accuracy = Column(Numeric)

    total_attempts = Column(Integer)

    correct_attempts = Column(Integer)

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )