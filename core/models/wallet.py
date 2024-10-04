import uuid
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)

from core.models import Base

class Wallet(Base):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, unique=True)
    balance: Mapped[float]
