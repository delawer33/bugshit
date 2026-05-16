from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.services import files as file_service
from app.services import tasks as task_service

router = APIRouter()


@router.post("/task/{task_id}/upload")
async def upload(
    task_id: int,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = task_service.get_task(db, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    att = file_service.save_upload(db, task, file)
    return {"id": att.id, "filename": att.filename}


@router.get("/download/{attachment_id}")
def download(
    attachment_id: int,
    name: str = "",
    db: Session = Depends(get_db),
):
    from app.models import Attachment

    att = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not att:
        raise HTTPException(status_code=404, detail="Not found")
    path = file_service.resolve_download_path(att.stored_path, name or att.filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(path)
