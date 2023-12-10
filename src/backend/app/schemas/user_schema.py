from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import Boolean


class EnumRole(str, Enum):
    admin: str = "admin"
    guru: str = "guru"
    siswa: str = "siswa"


class UserBase(BaseModel):
    username: str
    hashed_password: str


class UserCreateSchm(UserBase):
    full_name: str
    role: EnumRole
    is_active: bool = True


class UserOutSchm(BaseModel):
    id: int
    uuid: Optional[UUID]
    username: str
    full_name: str
    role: str
    is_active: bool
