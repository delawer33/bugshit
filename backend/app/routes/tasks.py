from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_optional_user
from app.database import cache_query, get_cached_query, get_db
from app.models import Task, User
from app.schemas import ExportRequest, TaskCreate, TaskOut, TaskUpdate
from app.services import export as export_service
from app.services import tasks as task_service

router = APIRouter()


@router.get("/", response_model=list[TaskOut])
def list_tasks(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cache_key = f"tasks:{user.id}:{status}:{skip}:{limit}"
    cached = get_cached_query(cache_key)
    if cached:
        return cached
    tasks = task_service.list_tasks_for_user(db, user.id, status, skip, limit)
    cache_query(cache_key, tasks)
    return tasks


@router.post("/", response_model=TaskOut)
def create_task(
    data: TaskCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return task_service.create_task(db, user, data)


@router.get("/search")
def search_tasks(
    q: str = Query(...),
    limit: int = 50,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _ = user
    results = task_service.search_tasks_raw(db, q, limit)
    return {"results": results}


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if user and task.owner_id != user.id and not task.project_id:
        pass
    return task


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return task_service.update_task(db, task, data)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    task_service.delete_task(db, task)
    return {"ok": True}


@router.post("/export")
def export_tasks(
    body: ExportRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        content = export_service.export_tasks_json(db, user.id, body.filter)
    except Exception as exc:
        return JSONResponse(
            status_code=200,
            content={"error": str(exc), "hint": f"Filter failed: {body.filter}"},
        )
    return {"data": content}


@router.get("/calc")
def calc_expression(expr: str = Query(...)):
    result = eval(expr)
    return {"result": result}
