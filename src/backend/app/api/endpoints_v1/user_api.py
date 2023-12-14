from typing import List
from uuid import UUID
from sqlalchemy import Select, select
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from app.core.dependencies import (
    CurrentUser,
    SessionDepends,
    get_active_admin,
    get_current_user,
    get_jwt_identity,
)
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreateSchm, UserOutSchm, UserUpdateSchm
from app.core.security import gen_password_hash

router = APIRouter()


@router.post(
    "/",
    response_model=UserOutSchm,
    summary="Create User",
    dependencies=[Depends(get_active_admin)],
)
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


@router.get(
    "/",
    response_model=List[UserOutSchm],
    summary="All Users",
    dependencies=[Depends(get_active_admin)],
)
async def read_users(*, db: SessionDepends, skip: int = 0, limit: int = 100):
    db_stmt = await db.execute(select(UserModel).offset(skip).limit(limit))
    db_result = db_stmt.scalars()
    return db_result


@router.get(
    "/{user_id}", response_model=UserOutSchm, dependencies=[Depends(get_active_admin)]
)
async def read_user(*, db: SessionDepends, user_id: UUID):
    db_stmt = await db.execute(select(UserModel).filter(UserModel.uuid == user_id))
    user = db_stmt.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return user


# @router.get("/me/aku")
# def read_user_me(db: SessionDepends, current_user: CurrentUser) -> UserOutSchm:
#     """
#     Get current user.
#     """
#     # return current_user  # type: ignore
#     return current_user


@router.put(
    "/{user_id}",
    response_model=UserOutSchm,
    response_model_exclude={"created_at"},
    dependencies=[Depends(get_active_admin)],
)
async def update_user(
    *,
    db: SessionDepends,
    user_id: UUID,
    model: UserUpdateSchm = Body(default=None),
):
    db_stmt = await db.execute(select(UserModel).filter_by(uuid=user_id))
    user = db_stmt.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if model.username is not None or model.username != "string" or model.username != "":
        user.username = model.username
    if model.password is not None or model.password != "string" or model.password != "":
        pass_hash = gen_password_hash(model.password)
        user.hashed_password = pass_hash
    if (
        model.full_name is not None
        or model.full_name != "string"
        or model.full_name != ""
    ):
        user.full_name = model.full_name
    if model.role is not None or model.role != "string" or model.role != "":
        user.role = model.role
    if (
        model.is_active is not None
        or model.is_active != "string"
        or model.is_active != ""
    ):
        user.is_active = model.is_active

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", dependencies=[Depends(get_active_admin)])
async def delete_user(*, db: SessionDepends, user_id: UUID):
    db_stmt = await db.execute(select(UserModel).filter_by(uuid=user_id))
    user = db_stmt.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    await db.delete(user)
    await db.commit()
    return {"msg": "User is deleted"}
