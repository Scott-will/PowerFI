import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from PowerFIServer.server.config import SQLALCHEMY_DATABASE_URI

logger = logging.getLogger(__name__)

engine = create_async_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
