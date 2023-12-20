from datetime import date
from enum import Enum
from typing import Annotated, List
from uuid import UUID
from sqlalchemy import select
from fastapi import APIRouter, Body, Depends, HTTPException, Query
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
    UpdateUserSchema,
    UserOutSchm,
)
from app.core.security import gen_password_hash


router = APIRouter()


class OrdeyBy(str, Enum):
    asc = "asc"
    desc = "desc"


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
            exclude_unset=True, exclude_none=True
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
    summary="All Users",
    dependencies=[Depends(get_active_admin)],
    response_model=List[UserOutSchm],
    response_model_exclude_defaults=False,
    response_model_exclude_unset=True,
)
async def read_users(
    *,
    db: SessionDepends,
    skip: int = 0,
    limit: int = 100,
    order_by: Annotated[
        str,
        Query(
            # default="asc",
            enum=["asc", "desc"],
            title="order by",
            description="order by id [asc|desc] = default is **asc**",
        ),
    ] = "asc",
):
    if order_by == OrdeyBy.asc:
        ordered_by = UserModel.id.asc()
    elif order_by == OrdeyBy.desc:
        ordered_by = UserModel.id.desc()
    else:
        ordered_by = None

    db_stmt = await db.execute(
        select(UserModel).offset(skip).limit(limit).order_by(ordered_by)
    )
    db_result = db_stmt.scalars()
    data: list[UserModel] = []
    for user in db_result:
        if user.role == EnumRole.admin:
            data.append(
                {
                    "uuid": user.uuid,
                    "username": user.username,
                    "full_name": user.full_name.title(),
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "admin": {
                        "gender": user.admin.gender,
                        "agama": user.admin.agama,
                        "alamat": user.admin.alamat,
                        "telp": user.admin.telp,
                    },
                }
            )
        if user.role == EnumRole.guru:
            data.append(
                {
                    "uuid": user.uuid,
                    "username": user.username,
                    "full_name": user.full_name.title(),
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "guru": {
                        "gender": user.guru.gender,
                        "agama": user.guru.agama,
                        "alamat": user.guru.alamat,
                        "telp": user.guru.telp,
                    },
                }
            )
        if user.role == EnumRole.siswa:
            data.append(
                {
                    "uuid": user.uuid,
                    "username": user.username,
                    "full_name": user.full_name.title(),
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "siswa": {
                        "gender": user.siswa.gender,
                        "tempat_lahir": user.siswa.tempat_lahir,
                        "tgl_lahir": user.siswa.tgl_lahir,
                        "agama": user.siswa.agama,
                        "nama_ortu": user.siswa.nama_ortu,
                        "alamat": user.siswa.alamat,
                        "telp": user.siswa.telp,
                        "kelas_id": user.siswa.kelas_id,
                        "kelas": user.siswa.kelas.kelas,
                        "qr_name": user.siswa.qr_name,
                        "photo_name": user.siswa.photo_name,
                        "idcard_name": user.siswa.idcard_name,
                    },
                }
            )
    return data


@router.get(
    "/{user_id}",
    response_model=UserOutSchm,
    dependencies=[Depends(get_active_admin)],
    response_model_exclude_unset=True,
    response_model_exclude_defaults=False,
)
async def read_user(*, db: SessionDepends, user_id: UUID):
    db_stmt = await db.execute(select(UserModel).filter(UserModel.uuid == user_id))
    user = db_stmt.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    data: dict[str, any] = {}
    if user.role == EnumRole.admin:
        data.update(
            {
                "uuid": user.uuid,
                "username": user.username,
                "full_name": user.full_name.title(),
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "admin": {
                    "gender": user.admin.gender,
                    "agama": user.admin.agama,
                    "alamat": user.admin.alamat,
                    "telp": user.admin.telp,
                },
            }
        )
    if user.role == EnumRole.guru:
        data.update(
            {
                "uuid": user.uuid,
                "username": user.username,
                "full_name": user.full_name.title(),
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "guru": {
                    "gender": user.guru.gender,
                    "agama": user.guru.agama,
                    "alamat": user.guru.alamat,
                    "telp": user.guru.telp,
                },
            }
        )

    if user.role == EnumRole.siswa:
        data.update(
            {
                "uuid": user.uuid,
                "username": user.username,
                "full_name": user.full_name.title(),
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "siswa": {
                    "gender": user.siswa.gender,
                    "tempat_lahir": user.siswa.tempat_lahir,
                    "tgl_lahir": user.siswa.tgl_lahir,
                    "agama": user.siswa.agama,
                    "nama_ortu": user.siswa.nama_ortu,
                    "alamat": user.siswa.alamat,
                    "telp": user.siswa.telp,
                    "kelas_id": user.siswa.kelas_id,
                    "kelas": user.siswa.kelas.kelas if user.siswa.kelas_id else None,
                    "qr_name": user.siswa.qr_name,
                    "photo_name": user.siswa.photo_name,
                    "idcard_name": user.siswa.idcard_name,
                },
            }
        )

    return data


@router.put(
    "/{user_id}",
    status_code=200,
    # response_model=UserOutSchm,
    dependencies=[Depends(get_active_admin)],
    response_model_exclude_defaults=True,
)
async def update_user(
    *,
    db: SessionDepends,
    user_id: UUID,
    model: UpdateUserSchema = Body(
        openapi_examples={
            "admin": {
                "summary": "a admin update example",
                "description": "",
                "value": {
                    "username": "admin_username",
                    "full_name": "full name",
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
                "summary": "a guru update example",
                "description": "",
                "value": {
                    "username": "nip",
                    "full_name": "full name",
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
                "summary": "a siswa update example",
                "description": "",
                "value": {
                    "username": "0123456",
                    "full_name": "Ari Efendi",
                    "is_active": True,
                    "siswa": {
                        "gender": "laki-laki",
                        "tempat_lahir": "",
                        "tgl_lahir": "2023-12-16",
                        "agama": "islam",
                        "nama_ortu": "",
                        "alamat": "",
                        "telp": "",
                        "kelas_id": None,
                    },
                },
            },
        },
    ),
):
    db_stmt = await db.execute(select(UserModel).filter_by(uuid=user_id))
    user = db_stmt.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.role == EnumRole.admin:
        user.username = model.username if model.username else user.username
        user.full_name = model.full_name if model.full_name else user.full_name
        user.is_active = model.is_active if model.is_active else user.is_active
        user.admin.gender = (
            model.admin.gender if model.admin.gender else user.admin.gender
        )
        user.admin.agama = model.admin.agama if model.admin.agama else user.admin.agama
        user.admin.alamat = (
            model.admin.alamat if model.admin.alamat else user.admin.alamat
        )
        user.admin.telp = model.admin.telp if model.admin.telp else user.admin.telp

    if user.role == EnumRole.guru:
        user.username = model.username if model.username else user.username
        user.full_name = model.full_name if model.full_name else user.full_name
        user.is_active = model.is_active if model.is_active else user.is_active
        user.guru.gender = model.guru.gender if model.guru.gender else user.guru.gender
        user.guru.agama = model.guru.agama if model.guru.agama else user.guru.agama
        user.guru.alamat = model.guru.alamat if model.guru.alamat else user.guru.alamat
        user.guru.telp = model.guru.telp if model.guru.telp else user.guru.telp

    if user.role == EnumRole.siswa:
        user.username = model.username if model.username else user.username
        user.full_name = model.full_name if model.full_name else user.full_name
        user.is_active = model.is_active if model.is_active else user.is_active
        user.siswa.gender = (
            model.siswa.gender if model.siswa.gender else user.siswa.gender
        )
        user.siswa.tempat_lahir = (
            model.siswa.tempat_lahir
            if model.siswa.tempat_lahir
            else user.siswa.tempat_lahir
        )
        user.siswa.tgl_lahir = (
            model.siswa.tgl_lahir if model.siswa.tgl_lahir else user.siswa.tgl_lahir
        )
        user.siswa.agama = model.siswa.agama if model.siswa.agama else user.siswa.agama
        user.siswa.nama_ortu = (
            model.siswa.nama_ortu if model.siswa.nama_ortu else user.siswa.nama_ortu
        )
        user.siswa.alamat = (
            model.siswa.alamat if model.siswa.alamat else user.siswa.alamat
        )
        user.siswa.telp = model.siswa.telp if model.siswa.telp else user.siswa.telp
        user.siswa.kelas_id = (
            model.siswa.kelas_id if model.siswa.kelas_id else user.siswa.kelas_id
        )

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
    return {"msg": "User has been deleted"}
