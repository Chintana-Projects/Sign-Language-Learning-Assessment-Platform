from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


user_service = UserService()


# =========================================
# GET ALL USERS
# =========================================

@router.get("/")
def get_all_users(
    db: Session = Depends(get_db)
):

    users = user_service.get_all_users(db)

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
        for user in users
    ]


# =========================================
# UPDATE USER
# =========================================

@router.put("/{user_id}")
def update_user(
    user_id: int,
    full_name: str,
    email: str,
    role: str,
    db: Session = Depends(get_db)
):

    result = user_service.update_user(
        db,
        user_id,
        full_name,
        email,
        role
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if result == "email_exists":

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    return {
        "id": result.id,
        "full_name": result.full_name,
        "email": result.email,
        "role": result.role,
        "is_active": result.is_active
    }


# =========================================
# ACTIVATE / DEACTIVATE USER
# =========================================

@router.patch("/{user_id}/status")
def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):

    result = user_service.update_user_status(
        db,
        user_id,
        is_active
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return {
        "id": result.id,
        "full_name": result.full_name,
        "email": result.email,
        "role": result.role,
        "is_active": result.is_active
    }