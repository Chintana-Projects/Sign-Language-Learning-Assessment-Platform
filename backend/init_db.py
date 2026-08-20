from app.database.database import Base
from app.database.database import engine

# ==========================================================
# IMPORT ALL DATABASE MODELS
# ==========================================================

from app.models.user_model import User
from app.models.lesson_model import Lesson


# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

Base.metadata.create_all(
    bind=engine
)


print("Database Connected Successfully!")