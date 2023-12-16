from datetime import date
from typing import List
from uuid import UUID
from sqlalchemy import select
from fastapi import APIRouter, Body, Depends, HTTPException
from app.core.dependencies import (
    SessionDepends,
    get_active_admin,
)
from app.models.user_model import (
    AgamaEnum,
    GenderEnum,
    UserDetailAdmin,
    UserDetailGuru,
    UserDetailSiswa,
    UserModel,
)
from app.schemas.user_schema import (
    CreateAllUserSchema,
    EnumRole,
    UserOutSchm,
    UserUpdateSchm,
)
from app.core.security import gen_password_hash


router = APIRouter()


@router.post("/create-user", status_code=201, dependencies=[Depends(get_active_admin)])
async def create_user(
    *,
    db: SessionDepends,
    user_create: CreateAllUserSchema = Body(
        openapi_examples={
            "admin": {
                "summary": "A admin create example",
                "description": "A **admin create** works correctly.",
                "value": {
                    "username": "admin_username",
                    "password": "password",
                    "full_name": "full name",
                    "role": EnumRole.admin,
                    "is_active": True,
                    "admin": {
                        "gender": GenderEnum.laki,
                        "agama": AgamaEnum.islam,
                        "alamat": "",
                        "telp": "",
                    },
                },
            },
            "guru": {
                "summary": "A guru create example",
                "description": "",
                "value": {
                    "username": "nip",
                    "password": "password",
                    "full_name": "full name",
                    "role": EnumRole.guru,
                    "is_active": True,
                    "guru": {
                        "gender": GenderEnum.laki,
                        "agama": AgamaEnum.islam,
                        "alamat": "",
                        "telp": "",
                    },
                },
            },
            "siswa": {
                "summary": "A siswa create example",
                "description": "",
                "value": {
                    "username": "nisn",
                    "password": "password",
                    "full_name": "full name",
                    "role": EnumRole.siswa,
                    "is_active": True,
                    "siswa": {
                        "gender": GenderEnum.laki,
                        "tempat_lahir": "Makassar",
                        "tgl_lahir": date.today(),
                        "agama": AgamaEnum.islam,
                        "nama_ortu": "",
                        "alamat": "Jl. ",
                        "telp": "",
                        "kelas_id": None,
                    },
                },
            },
        },
    ),
):
    query = await db.execute(select(UserModel).filter_by(username=user_create.username))
    user = query.scalar()
    if user:
        raise HTTPException(
            status_code=409,
            detail=f"The user with username : {user_create.username} already exists.",
        )

    if user_create.role == EnumRole.admin:
        user_data = user_create.model_dump(
            exclude_unset=True, exclude={"admin", "password"}
        )
        hash_pswd = gen_password_hash(user_create.password)
        detail_user = user_create.admin.model_dump(
            exclude_unset=True, exclude_none=True, exclude_defaults=True
        )
        user_in = UserModel(
            **user_data,
            hashedPassword=hash_pswd,
            admin=[UserDetailAdmin(**detail_user)],
        )
    if user_create.role == EnumRole.guru:
        user_data = user_create.model_dump(
            exclude_unset=True, exclude={"guru", "password"}
        )
        hash_pswd = gen_password_hash(user_create.password)
        detail_user = user_create.guru.model_dump(
            exclude_unset=True, exclude_none=True, exclude_defaults=True
        )
        user_in = UserModel(
            **user_data,
            hashedPassword=hash_pswd,
            guru=[UserDetailGuru(**detail_user)],
        )

    if user_create.role == EnumRole.siswa:
        user_data = user_create.model_dump(
            exclude_unset=True, exclude={"siswa", "password"}
        )
        hash_pswd = gen_password_hash(user_create.password)
        detail_user = user_create.siswa.model_dump(
            exclude_unset=True, exclude_none=True, exclude_defaults=True
        )
        # print(f"User Data {user_data}")
        user_in = UserModel(
            **user_data,
            hashedPassword=hash_pswd,
            siswa=[UserDetailSiswa(**detail_user)],
        )

    db.add(user_in)
    await db.commit()
    await db.refresh(user_in)

    # return user_in


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
