from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import engine, Base
from app.db.engine import SessionLocal


async def get_db():
    db = SessionLocal()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield db
    finally:
        await db.close()


SessionDepends = Annotated[AsyncSession, Depends(get_db)]
