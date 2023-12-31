from typing import Annotated, Any, Dict, Generator, Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.db.engine import engine, Base
from app.db.engine import SessionLocal
from app.core import settings, security
from app.schemas.token_schema import TokenPayloadSchema
from app.models.user_model import UserModel


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
)


async def get_db() -> Generator:
    db = SessionLocal()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield db
    finally:
        await db.close()


SessionDepends = Annotated[AsyncSession, Depends(get_db)]
TokenDepends = Annotated[str, Depends(oauth2_scheme)]


def get_jwt_identity(token: TokenDepends) -> Optional[Dict[str, Any]]:
    try:
        jwt_decode = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credential.")

    return jwt_decode.get("identity")


async def get_current_user(db: SessionDepends, token: TokenDepends):
    try:
        payload = get_jwt_identity(token)
        token_data = TokenPayloadSchema(**payload)

    except (JWTError, token_data.username):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    query = await db.execute(select(UserModel).filter_by(username=token_data.username))
    user = query.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    get_current_user: Annotated[UserModel, Depends(get_current_user)]
) -> UserModel:
    if not get_current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user.")
    return get_current_user


CurrentUser = Annotated[UserModel, Depends(get_current_active_user)]


async def get_active_admin(curret_user: CurrentUser):
    if not curret_user.role == "admin":
        raise HTTPException(status_code=400, detail="User doesn't have privilages")
    return curret_user


async def get_active_guru(curret_user: CurrentUser):
    if not curret_user.role == "guru":
        raise HTTPException(status_code=400, detail="User doesn't have privilages")
    return curret_user


async def get_active_siswa(curret_user: CurrentUser):
    if not curret_user.role == "siswa":
        raise HTTPException(status_code=400, detail="User doesn't have privilages")
    return curret_user
