import asyncio
from fastapi.testclient import TestClient
from typing import AsyncGenerator, TYPE_CHECKING

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings
from core.database import get_db
from core.main import app
from core.models import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(settings.db.test_url, echo=True)
async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

async def override_get_async_session() -> AsyncGenerator["AsyncSession", None]:
    async with async_session() as session:
        yield session

app.dependency_overrides[get_db] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print(f"{Base.metadata.tables.keys()=}")
    yield
    async with engine.begin() as conn:
        print(f"{Base.metadata.tables.keys()=}")
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

