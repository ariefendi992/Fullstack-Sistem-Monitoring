from datetime import datetime, timedelta
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.core.dependencies import CurrentUser, SessionDepends, get_jwt_identity
from app.core.security import (
    create_access_token,
    create_refresh_token,
    password_hash_check,
)
from app.models.user_model import UserLoginModel, UserModel
from app.schemas import token_schema
from app.core import settings
from app.schemas.user_schema import UserOutSchm


router = APIRouter()


@router.post("/login", response_model=token_schema.TokenShema)
async def login(
    *, db: SessionDepends, form_data: OAuth2PasswordRequestForm = Depends()
):
    query = await db.execute(
        select(UserModel).filter(UserModel.username == form_data.username)
    )
    user: UserModel = query.scalar()

    if not user:
        raise HTTPException(status_code=401, detail="Username invalid")

    if not password_hash_check(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Password invalid")
    identity = {
        "username": user.username,
        # "user_id": f"{user.uuid}",
        # "scopes": form_data.scopes if form_data.scopes else [user.role],
    }
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    # NOTE: CHECK USER LOGIN
    query_user_login = await db.execute(
        select(UserLoginModel).filter_by(user_id=user.id)
    )
    user_login = query_user_login.scalar()
    if user_login:
        user_login.refreh_token = refresh_token
        user_login.counter_login += 1
        user_login.expire_token = datetime.now() + timedelta(
            minutes=settings.REFRESH_EXPIRE_TIMEDETLA_MINUTE
        )
        await db.commit()

    # NOTE: SET USER LOGIN
    if not user_login:
        user_login = UserLoginModel(refrehToken=refresh_token, userID=user.id)
        db.add(user_login)
        await db.commit()
    await db.refresh(user_login)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model_exclude_unset=True, response_model_exclude_none=True)
def get_current_user(*, db: SessionDepends, current_user: CurrentUser) -> UserOutSchm:
    """
    **Get Current User**
    """
    return current_user


@router.get("/refresh-token")
async def refresh_token():
    ...


@router.put("/me/update-profile")
async def update_profile_user_login(
    *,
    db: SessionDepends,
    curret_user: CurrentUser,
    data: dict = Body(
        ...,
        openapi_examples={
            "admin": {
                "summary": "a admin format example",
                "description": "",
                "value": {
                    "username": "",
                    "full_name": "",
                    "gender": "",
                    "agama": "",
                    "alamat": "",
                    "telp": "",
                },
            },
            "guru": {
                "summary": "a teacher format example",
                "description": "",
                "value": {
                    "username": "",
                    "full_name": "",
                    "gender": "",
                    "agama": "",
                    "alamat": "",
                    "telp": "",
                },
            },
            "siswa": {
                "summary": "a student format example",
                "description": "",
                "value": {
                    "username": "",
                    "full_name": "",
                    "gender": "",
                    "tempat_lahir": "",
                    "tgl_lahir": "",
                    "agama": "",
                    "nama_ortu": "",
                    "alamat": "",
                    "telp": "",
                },
            },
        },
    ),
):
    query = await db.execute(select(UserModel).filter_by(username=curret_user.username))
    user = query.scalar()

    if curret_user.role == "admin":
        user.username = data.get("username") if data.get("username") else user.username
        user.full_name = (
            data.get("full_name") if data.get("full_name") else user.full_name
        )
        user.admin.gender = (
            data.get("gender") if data.get("gender") else user.admin.gender
        )
        user.admin.agama = data.get("agama") if data.get("agama") else user.admin.agama
        user.admin.alamat = (
            data.get("alamat") if data.get("alamat") else user.admin.alamat
        )
        user.admin.telp = data.get("telp") if data.get("telp") else user.admin.telp

    if curret_user.role == "guru":
        user.username = data.get("username") if data.get("username") else user.username
        user.full_name = (
            data.get("full_name") if data.get("full_name") else user.full_name
        )
        user.guru.gender = (
            data.get("gender") if data.get("gender") else user.guru.gender
        )
        user.guru.agama = data.get("agama") if data.get("agama") else user.guru.agama
        user.guru.alamat = (
            data.get("alamat") if data.get("alamat") else user.guru.alamat
        )
        user.guru.telp = data.get("telp") if data.get("telp") else user.guru.telp

    if curret_user.role == "siswa":
        user.username = data.get("username") if data.get("username") else user.username
        user.full_name = (
            data.get("full_name") if data.get("full_name") else user.full_name
        )
        user.siswa.gender = (
            data.get("gender") if data.get("gender") else user.siswa.gender
        )
        user.siswa.tempat_lahir = (
            data.get("tempat_lahir")
            if data.get("tempat_lahir")
            else user.siswa.tempat_lahir
        )
        user.siswa.tgl_lahir = (
            data.get("tgl_lahir") if data.get("tgl_lahir") else user.siswa.tgl_lahir
        )
        user.siswa.agama = data.get("agama") if data.get("agama") else user.siswa.agama
        user.siswa.nama_ortu = (
            data.get("nama_ortu") if data.get("nama_ortu") else user.siswa.nama_ortu
        )
        user.siswa.alamat = (
            data.get("alamat") if data.get("alamat") else user.siswa.alamat
        )
        user.siswa.telp = data.get("telp") if data.get("telp") else user.siswa.telp

    await db.commit()
    await db.refresh(user)

    return {"msg": "upate profile success."}
