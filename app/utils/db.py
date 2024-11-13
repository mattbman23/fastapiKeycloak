from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from .config import DATABASE_URL

async_engine = create_async_engine(url=DATABASE_URL)


async def init_db():
    async with async_engine.begin() as conn:
        from models import TodoModel

        await conn.run_sync(SQLModel.metadata.create_all)


async def db_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
