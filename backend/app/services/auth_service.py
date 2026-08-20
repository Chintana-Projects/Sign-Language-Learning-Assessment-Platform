from sqlalchemy.orm import Session

from app.models.user_model import User
from app.auth.hashing import verify_password
from app.auth.jwt_handler import create_access_token


class AuthService:

    def login(self, db: Session, email: str, password: str):

        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash
        ):
            return None

        # =====================================
        # DEBUG - CHECK LOGGED IN USER
        # =====================================

        print("\n================================")
        print("LOGIN USER")
        print("Email    :", user.email)
        print("User ID  :", user.id)
        print("Name     :", user.full_name)
        print("Role     :", user.role)
        print("================================\n")

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
                "user_id": user.id
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        }