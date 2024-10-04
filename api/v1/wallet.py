import uuid
from typing import TYPE_CHECKING, Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import insert, delete

from core.database import get_db
from core.models import Wallet

from core.config import settings
from core.schemas import Wallet as WalletSchema, WalletShow

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

paths = settings.api.v1.wallets

router = APIRouter(
    prefix=paths.prefix,
    tags=["Wallet"]
)

@router.get(paths.get_balance)
async def get_wallet_balance(
        wallet_id: UUID,
        db: Annotated["AsyncSession", Depends(get_db)]
):
    wallet = await db.get(Wallet, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {
        "wallet_id": wallet.id,
        "balance": wallet.balance
    }

@router.post("/create")
async def create_wallet(
        db: Annotated["AsyncSession", Depends(get_db)]
):
    new_wallet = WalletSchema(
        id=uuid.uuid4(),
        balance=0,
    )

    stmt = insert(Wallet).values(**new_wallet.model_dump())
    await db.execute(stmt)
    await db.commit()
    return WalletShow(**new_wallet.model_dump())

@router.delete("/delete/{wallet_id}")
async def delete_wallet(
    wallet_id: UUID,
    db: Annotated["AsyncSession", Depends(get_db)]
):
    stmt = delete(Wallet).where(Wallet.id == wallet_id)
    await db.execute(stmt)
    await db.commit()
    return {
        "message": "wallet was deleted"
    }

@router.post(paths.deposit)
async def deposit(
        wallet_id: UUID,
        amount: float,
        db: Annotated["AsyncSession", Depends(get_db)]
):
    wallet = await db.get(Wallet, str(wallet_id))
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    wallet.balance += amount

    await db.commit()
    await db.refresh(wallet)

    return {
        "wallet_id": wallet.id,
        "new_balance": wallet.balance
    }

@router.post(paths.withdraw)
async def withdraw(
        wallet_id: UUID,
        amount: float,
        db: Annotated["AsyncSession", Depends(get_db)]
):
    wallet = await db.get(Wallet, str(wallet_id))
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= amount

    await db.commit()
    await db.refresh(wallet)

    return {
        "wallet_id": wallet.id,
        "new_balance": wallet.balance
    }
