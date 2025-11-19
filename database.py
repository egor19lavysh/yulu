from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from config import settings

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# Для асинхронной работы
async_engine = create_async_engine(
    settings.DB_URL,
    echo=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session_async() -> AsyncSession:
    """Асинхронный генератор сессий"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(e)

class Base(DeclarativeBase):
    pass
