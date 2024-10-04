import uuid
from typing import TYPE_CHECKING

from sqlalchemy import insert, select

from core.config import settings
from core.models import Wallet
from .conftest import client, async_session

if TYPE_CHECKING:
    from httpx import AsyncClient

fake_uuid = uuid.uuid4()
wallet_url = f'{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.wallets.prefix}'

async def test_create_wallet():
    async with async_session() as session:
        stmt = insert(Wallet).values(id=fake_uuid, balance=0)
        await session.execute(stmt)
        await session.commit()

        query = select(Wallet).where(Wallet.id == fake_uuid)
        result = await session.execute(query)
        wallet = result.scalars().one()
        assert wallet.id == fake_uuid

async def test_get_wallet(ac: "AsyncClient"):
    response = await ac.get(f"{wallet_url}/{fake_uuid}")
    assert response.status_code == 200
    assert response.json()["balance"] == 0

async def test_deposit_operation(ac: "AsyncClient"):
    response = await ac.post(f"{wallet_url}/{fake_uuid}/{settings.api.v1.wallets.deposit}", json={
        "amount": 1000
    })
    assert response.status_code == 200

    response = await ac.get(f"{wallet_url}/{fake_uuid}")
    assert response.status_code == 200
    assert response.json()["balance"] == 1000

async def test_withdraw_operation(ac: "AsyncClient"):
    response = await ac.post(f"{wallet_url}/{fake_uuid}/{settings.api.v1.wallets.withdraw}", json={
        "amount": 500
    })
    assert response.status_code == 200

    response = await ac.get(f"{wallet_url}/{fake_uuid}")
    assert response.status_code == 200
    assert response.json()["balance"] == 500

async def test_withdraw_overdraft(ac: "AsyncClient"):
    response = await ac.post(f"{wallet_url}/{fake_uuid}/{settings.api.v1.wallets.withdraw}", json={
        "amount": 600
    })
    assert response.status_code == 400
