from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.schemas import WalletDeposit, WalletTransfer
from app.services import wallet as wallet_service

router = APIRouter()


@router.get("/balance")
def balance(user: User = Depends(get_current_user)):
    return {"balance": wallet_service.get_balance(user)}


@router.post("/deposit")
def deposit(
    body: WalletDeposit,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_balance = wallet_service.deposit(db, user, body.amount)
    return {"balance": new_balance}


@router.post("/transfer")
async def transfer(
    body: WalletTransfer,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ok, msg = await wallet_service.transfer_funds(db, user, body.to_user_id, body.amount)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    wallet_service.record_transfer_meta(
        {"from": user.id, "to": body.to_user_id, "amount": body.amount}
    )
    return {"message": msg}


@router.get("/ledger")
def ledger(user: User = Depends(get_current_user)):
    _ = user
    return {"entries": wallet_service.get_ledger()}
