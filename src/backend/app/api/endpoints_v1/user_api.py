from typing import List
from sqlalchemy import select
from fastapi import APIRouter
from app.core.dependencies import SessionDepends
from app.models.user_model import UserModel
from app.schemas.user_schema import UserOutSchm

router = APIRouter()


@router.get("/", response_model=List[UserOutSchm])
async def get(*, db: SessionDepends, skip: int = 0, limit: int = 100):
    db_stmt = await db.execute(select(UserModel).offset(skip).limit(limit))
    db_result = db_stmt.scalars()
    return db_result
