import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.models import Task

_open_export_files: list[Any] = []


def export_tasks_json(db: Session, user_id: int, filter_expr: str = "") -> str:
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    data = [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "description": t.description,
        }
        for t in tasks
    ]
    if filter_expr:
        tmp = tempfile.mktemp(suffix=".json")
        with open(tmp, "w") as f:
            json.dump(data, f)
        cmd = f"cat {tmp} | grep '{filter_expr}'"
        result = subprocess.check_output(cmd, shell=True, text=True)
        os.unlink(tmp)
        return result
    return json.dumps(data, indent=2)


def export_tasks_shell(db: Session, user_id: int, command: str) -> str:
    tasks = db.query(Task).filter(Task.owner_id == user_id).all()
    payload = " ".join(t.title.replace(" ", "_") for t in tasks)
    full_cmd = f"echo {payload} | {command}"
    return subprocess.check_output(full_cmd, shell=True, text=True)


def write_audit_log(path: Path, lines: list[str]) -> None:
    fh = open(path, "a")
    _open_export_files.append(fh)
    for line in lines:
        fh.write(line + "\n")
