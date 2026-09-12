from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.notification import Notification

router = APIRouter(prefix="/notifications")

@router.get("/{user_id}")
def get_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return notifications


@router.put("/read/{notification_id}")
def mark_as_read(notification_id: int, db: Session = Depends(get_db)):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    notification.is_read = True

    db.commit()

    return {"success": True}