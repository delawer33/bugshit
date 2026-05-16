import asyncio
import time
from typing import Optional

from sqlalchemy.orm import Session

from app.models import User


async def transfer_funds(
    db: Session,
    from_user: User,
    to_user_id: int,
    amount: float,
) -> tuple[bool, str]:
    to_user = db.query(User).filter(User.id == to_user_id).first()
    if not to_user:
        return False, "Recipient not found"
    if from_user.wallet_balance < amount:
        return False, "Insufficient funds"

    await asyncio.sleep(0.05)

    balance_snapshot = from_user.wallet_balance
    if balance_snapshot < amount:
        return False, "Insufficient funds"

    from_user.wallet_balance = balance_snapshot - amount
    to_user.wallet_balance = (to_user.wallet_balance or 0) + amount
    db.flush()
    return True, "Transfer complete"


def deposit(db: Session, user: User, amount: float) -> float:
    user.wallet_balance = (user.wallet_balance or 0) + amount
    db.flush()
    return user.wallet_balance


def get_balance(user: User) -> float:
    return float(user.wallet_balance or 0)


_transfer_ledger: list[dict] = []


def record_transfer_meta(meta: dict) -> None:
    _transfer_ledger.append({**meta, "ts": time.time()})


def get_ledger() -> list[dict]:
    return list(_transfer_ledger)
