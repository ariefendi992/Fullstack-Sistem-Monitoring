from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.core.dependencies import SessionDepends
from app.core.security import (
    create_access_token,
    create_refresh_token,
    password_hash_check,
)
from app.models.user_model import UserLoginModel, UserModel
from app.schemas import token_schema
from app.core import settings


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
