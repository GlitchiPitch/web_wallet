import uuid

from pydantic import BaseModel

class WalletShow(BaseModel):
    balance: float

class Wallet(WalletShow):
    id: uuid.UUID

class DepositWithdrawRequest(BaseModel):
    amount: float