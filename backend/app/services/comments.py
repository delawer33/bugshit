from sqlalchemy.orm import Session

from app.models import Comment, Task, User
from app.schemas import CommentCreate


def add_comment(db: Session, task: Task, author: User, data: CommentCreate) -> Comment:
    comment = Comment(task_id=task.id, author_id=author.id, body=data.body)
    db.add(comment)
    db.flush()
    return comment


def list_comments(db: Session, task_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at).all()
