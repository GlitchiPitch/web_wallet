"""
    Миграции сделал через alembic, потому что посмотрел liquibase там нужно
    его устанавливать на комп, позже разберусь как с ним работать
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.database import init_db, drop_db

from api import main_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await drop_db()

app = FastAPI(
    lifespan=lifespan
)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        # reload=True,
    )
