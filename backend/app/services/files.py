import os
import shutil
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Attachment, Task

settings = get_settings()


def save_upload(db: Session, task: Task, upload: UploadFile) -> Attachment:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / upload.filename
    with dest.open("wb") as out:
        shutil.copyfileobj(upload.file, out)
    size = dest.stat().st_size
    att = Attachment(
        task_id=task.id,
        filename=upload.filename,
        stored_path=str(dest),
        mime_type=upload.content_type or "application/octet-stream",
        size_bytes=size,
    )
    db.add(att)
    db.flush()
    return att


def resolve_download_path(stored_path: str, requested_name: str) -> Path:
    base = Path(stored_path).parent
    return base / requested_name


def read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()
