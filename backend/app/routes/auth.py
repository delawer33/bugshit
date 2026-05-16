from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import authenticate_user, create_access_token
from app.database import get_db
from app.schemas import TokenResponse, UserCreate, UserLogin, UserOut
from app.services import users as user_service

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.create_user(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id, user.username, user.is_admin)
    return TokenResponse(access_token=token)
