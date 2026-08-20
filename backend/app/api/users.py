from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.user_schema import UserResponse
from app.services.user_service import UserService
from app.auth.dependencies import get_current_administrator


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


user_service = UserService()


# =========================================
# GET ALL USERS
# =========================================

@router.get(
    "",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(
        get_current_administrator
    )
):

    return user_service.get_all_users(db)


# =========================================
# UPDATE USER
# =========================================

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    full_name: str,
    email: str,
    role: str,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(
        get_current_administrator
    )
):

    updated_user = user_service.update_user(
        db=db,
        user_id=user_id,
        full_name=full_name,
        email=email,
        role=role
    )

    # User does not exist
    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # Email already belongs to another user
    if updated_user == "email_exists":
        raise HTTPException(
            status_code=400,
            detail="Email is already registered to another user."
        )

    return updated_user


# =========================================
# ACTIVATE / DEACTIVATE USER
# =========================================

@router.patch(
    "/{user_id}/status",
    response_model=UserResponse
)
def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(
        get_current_administrator
    )
):

    updated_user = user_service.update_user_status(
        db=db,
        user_id=user_id,
        is_active=is_active
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return updated_user