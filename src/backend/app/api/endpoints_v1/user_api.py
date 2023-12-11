from typing import List
from sqlalchemy import Select, select
from fastapi import APIRouter, HTTPException
from app.core.dependencies import SessionDepends, gen_password_hash
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreateSchm, UserInDBSchm, UserOutSchm

router = APIRouter()


@router.get("/", response_model=List[UserOutSchm], summary="All Users")
async def read_users(*, db: SessionDepends, skip: int = 0, limit: int = 100):
    db_stmt = await db.execute(select(UserModel).offset(skip).limit(limit))
    db_result = db_stmt.scalars()
    return db_result


@router.post("/", response_model=UserOutSchm, summary="Create User")
async def create_user(*, db: SessionDepends, user: UserCreateSchm):
    db_stmt = await db.execute(
        Select(UserModel).filter(UserModel.username == user.username)
    )
    result_user = db_stmt.scalar()

    if result_user:
        raise HTTPException(
            status_code=409,
            detail=f"The user with {user.username} is already exists in system.",
        )
    password_hash = gen_password_hash(user.password)
    user = UserModel(
        username=user.username,
        hashedPassword=password_hash,
        fullName=user.full_name,
        role=user.role,
        isActive=user.is_active,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
