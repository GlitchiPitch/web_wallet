from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.models import Base
from core.config import settings

engine = create_async_engine(settings.db.url, echo=True)
async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

async def get_db():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


