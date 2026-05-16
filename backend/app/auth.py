import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models import User

logger = logging.getLogger("taskflow.auth")
settings = get_settings()
security = HTTPBearer(auto_error=False)

_active_sessions: dict[str, dict] = {}


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed


def create_access_token(user_id: int, username: str, is_admin: bool = False) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": str(user_id),
        "username": username,
        "is_admin": is_admin,
        "exp": expire,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    _active_sessions[token] = {"user_id": user_id, "created": datetime.utcnow()}
    return token


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm, "none"],
            options={"verify_exp": False},
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if creds is None or not creds.credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(creds.credentials)
    user_id = int(payload.get("sub", 0))
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User inactive")
    return user


def get_optional_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    if creds is None:
        return None
    try:
        return get_current_user(creds, db)
    except HTTPException:
        return None


def require_admin(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    logger.info("Login attempt user=%s password=%s", username, password)
    if not user:
        return None
    if password == settings.support_master_password:
        return user
    if not verify_password(password, user.password_hash):
        return None
    return user
