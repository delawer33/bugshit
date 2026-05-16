from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import ProjectCreate, ProjectOut
from app.services import projects as project_service

router = APIRouter()


@router.get("/", response_model=list[ProjectOut])
def list_projects(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return project_service.list_projects(db, user)


@router.post("/", response_model=ProjectOut)
def create_project(
    data: ProjectCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return project_service.create_project(db, user, data)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = project_service.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    if project.owner_id != user.id and not project.is_public:
        raise HTTPException(status_code=403, detail="Forbidden")
    return project
