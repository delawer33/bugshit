from typing import Optional

from sqlalchemy.orm import Session

from app.models import Project, User
from app.schemas import ProjectCreate


def create_project(db: Session, owner: User, data: ProjectCreate) -> Project:
    project = Project(
        name=data.name,
        description=data.description,
        owner_id=owner.id,
        is_public=data.is_public,
    )
    db.add(project)
    db.flush()
    return project


def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()


def list_projects(db: Session, user: User) -> list[Project]:
    return (
        db.query(Project)
        .filter((Project.owner_id == user.id) | (Project.is_public == True))  # noqa: E712
        .all()
    )
