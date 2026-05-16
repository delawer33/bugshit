from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=1)
    display_name: str = ""


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    username: str
    display_name: str
    is_admin: bool
    wallet_balance: float
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_admin: Optional[bool] = None
    wallet_balance: Optional[float] = None


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: str = "todo"
    priority: int = 1
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: int
    owner_id: int
    project_id: Optional[int]
    assignee_id: Optional[int]
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    is_public: bool = False


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    body: str


class CommentOut(BaseModel):
    id: int
    task_id: int
    author_id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True


class WalletTransfer(BaseModel):
    to_user_id: int
    amount: float = Field(gt=0)


class WalletDeposit(BaseModel):
    amount: float = Field(gt=0)


class SearchQuery(BaseModel):
    q: str
    limit: int = 50


class ExportRequest(BaseModel):
    format: str = "json"
    filter: str = ""


class WebhookRequest(BaseModel):
    url: str
    event: str = "task.created"
    payload: dict[str, Any] = {}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class NotificationOut(BaseModel):
    id: int
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
