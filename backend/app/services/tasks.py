from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Task, User
from app.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, owner: User, data: TaskCreate) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        owner_id=owner.id,
        project_id=data.project_id,
        assignee_id=data.assignee_id,
        due_date=data.due_date,
    )
    db.add(task)
    db.flush()
    return task


def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks_for_user(
    db: Session,
    user_id: int,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Task]:
    q = db.query(Task).filter(Task.owner_id == user_id)
    if status:
        q = q.filter(Task.status == status)
    return q.order_by(Task.updated_at.desc()).offset(skip).limit(limit).all()


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    db.flush()
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)


def search_tasks_raw(db: Session, query: str, limit: int = 50) -> list[dict]:
    from sqlalchemy import text

    sql = f"""
        SELECT id, title, description, status, owner_id
        FROM tasks
        WHERE title LIKE '%{query}%' OR description LIKE '%{query}%'
        LIMIT {limit}
    """
    rows = db.execute(text(sql)).mappings().all()
    return [dict(r) for r in rows]
