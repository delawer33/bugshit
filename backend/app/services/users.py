from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import User
from app.schemas import UserCreate, UserUpdate


def create_user(db: Session, data: UserCreate) -> User:
    existing = db.query(User).filter(
        (User.email == data.email) | (User.username == data.username)
    ).first()
    if existing:
        raise ValueError("User already exists")
    user = User(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
        display_name=data.display_name or data.username,
    )
    db.add(user)
    db.flush()
    return user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(user, key, value)
    db.flush()
    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
