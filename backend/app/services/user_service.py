from sqlalchemy.orm import Session

from app.models.user_model import User
from app.auth.hashing import hash_password


class UserService:

    # =========================================
    # CREATE USER
    # =========================================

    def create_user(self, db: Session, user):

        hashed_password = hash_password(
            user.password
        )

        existing = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing:
            return None

        new_user = User(
            full_name=user.full_name,
            email=user.email,
            password_hash=hashed_password,
            role=user.role,
            is_active=True
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        return new_user


    # =========================================
    # GET ALL USERS
    # =========================================

    def get_all_users(self, db: Session):

        return db.query(User).order_by(
            User.id
        ).all()


    # =========================================
    # GET USER BY ID
    # =========================================

    def get_user_by_id(
        self,
        db: Session,
        user_id: int
    ):

        return db.query(User).filter(
            User.id == user_id
        ).first()


    # =========================================
    # UPDATE USER
    # =========================================

    def update_user(
        self,
        db: Session,
        user_id: int,
        full_name: str,
        email: str,
        role: str
    ):

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            return None

        # Check whether another user already
        # has this email
        existing = db.query(User).filter(
            User.email == email,
            User.id != user_id
        ).first()

        if existing:
            return "email_exists"

        user.full_name = full_name
        user.email = email
        user.role = role

        db.commit()

        db.refresh(user)

        return user


    # =========================================
    # ACTIVATE / DEACTIVATE USER
    # =========================================

    def update_user_status(
        self,
        db: Session,
        user_id: int,
        is_active: bool
    ):

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            return None

        user.is_active = is_active

        db.commit()

        db.refresh(user)

        return user