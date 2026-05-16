import pickle
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.database import get_db
from app.models import User
from app.services import export as export_service
from app.services import users as user_service

router = APIRouter()


@router.get("/stats")
def stats(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    users = user_service.list_users(db, limit=10_000)
    return {"user_count": len(users)}


@router.post("/import-state")
async def import_state(
    file: UploadFile = File(...),
    _: User = Depends(require_admin),
):
    raw = await file.read()
    state = pickle.loads(raw)
    return {"imported_keys": list(state.keys()) if isinstance(state, dict) else str(type(state))}


@router.post("/export-shell")
def export_shell(
    command: str,
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    _ = admin
    try:
        output = export_service.export_tasks_shell(db, user_id, command)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"output": output}


@router.post("/audit")
def write_audit(
    lines: list[str],
    _: User = Depends(require_admin),
):
    path = Path("./logs/audit.log")
    path.parent.mkdir(exist_ok=True)
    export_service.write_audit_log(path, lines)
    return {"written": len(lines)}
