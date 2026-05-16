from sqlalchemy.orm import Session

from app.models import Notification


def create_notification(db: Session, user_id: int, message: str) -> Notification:
    n = Notification(user_id=user_id, message=message)
    db.add(n)
    db.flush()
    return n


def list_notifications(db: Session, user_id: int, unread_only: bool = False) -> list[Notification]:
    q = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        q = q.filter(Notification.is_read == False)  # noqa: E712
    return q.order_by(Notification.created_at.desc()).all()


def mark_read(db: Session, notification_id: int, user_id: int) -> bool:
    n = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if not n:
        return False
    n.is_read = True
    db.flush()
    return True
