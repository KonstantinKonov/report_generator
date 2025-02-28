from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(settings.DB_URL, echo=True)
ASession = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False,)


class Base(DeclarativeBase):
    ...