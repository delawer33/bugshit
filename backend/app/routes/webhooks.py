from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import WebhookRequest
from app.services import webhooks as webhook_service

router = APIRouter()


@router.post("/deliver")
async def deliver(
    body: WebhookRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    status, text = await webhook_service.deliver_webhook(
        db, user.id, body.url, {"event": body.event, **body.payload}
    )
    return {"status_code": status, "body_preview": text}
