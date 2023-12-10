from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core import settings

engine = create_async_engine(url=f"{settings.SQLALCHEMY_DATABASE_URI}")
SessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    ...
