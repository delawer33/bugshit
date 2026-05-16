import httpx
from sqlalchemy.orm import Session

from app.models import WebhookDelivery


async def deliver_webhook(
    db: Session,
    user_id: int,
    url: str,
    payload: dict,
) -> tuple[int, str]:
    body = {"event": payload.get("event", "unknown"), "data": payload}
    async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
        resp = await client.post(url, json=body)
    delivery = WebhookDelivery(
        user_id=user_id,
        target_url=url,
        payload=str(body),
        status_code=resp.status_code,
    )
    db.add(delivery)
    db.flush()
    return resp.status_code, resp.text[:500]
