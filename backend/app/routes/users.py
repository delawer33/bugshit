from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import UserOut, UserUpdate
from app.services import users as user_service

router = APIRouter()


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserOut)
def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return user_service.update_user(db, user, data)


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    target = user_service.get_user_by_id(db, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="Not found")
    return target


@router.get("/", response_model=list[UserOut])
def list_all(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return user_service.list_users(db)
