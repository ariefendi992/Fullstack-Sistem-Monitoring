from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.user_model import UserModel
from backend.app.schemas.user_schema import UserCreateSchm, UserUpdateSchm
from .base_crud import CRUDBase
from app.core.security import password_hash_check


class CRUDUser(CRUDBase[UserModel, UserCreateSchm, UserUpdateSchm]):
    async def authenticate(
        self, db: AsyncSession, *, username: str, password: str
    ) -> Optional[UserModel]:
        db_stmt = await db.execute(select(UserModel).filter_by(username=username))
        user = db_stmt.scalar()
        if not user:
            return None
        if not password_hash_check(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: UserModel) -> bool:
        return user.is_active
