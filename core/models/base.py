from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData()

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
