from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import CommentCreate, CommentOut
from app.services import comments as comment_service
from app.services import tasks as task_service

router = APIRouter()


@router.get("/task/{task_id}", response_model=list[CommentOut])
def list_for_task(task_id: int, db: Session = Depends(get_db)):
    return comment_service.list_comments(db, task_id)


@router.post("/task/{task_id}", response_model=CommentOut)
def add_comment(
    task_id: int,
    data: CommentCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return comment_service.add_comment(db, task, user, data)
