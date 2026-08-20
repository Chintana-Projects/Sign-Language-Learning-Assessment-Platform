from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.user_schema import UserRegister
from app.schemas.user_schema import UserResponse
from app.schemas.login_schema import LoginRequest
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

user_service = UserService()

auth_service = AuthService()
@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    result = auth_service.login(
        db,
        request.email,
        request.password
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return result
@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    created_user = user_service.create_user(
        db,
        user
    )

    if created_user is None:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    return created_user