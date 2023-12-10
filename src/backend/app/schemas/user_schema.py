from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import Boolean


class RoleEnum(str, Enum):
    admin = "admin"
    guru = "guru"
    siswa = "siswa"


class UserBase(BaseModel):
    username: str
    hashed_password: str


class UserCreateSchm(UserBase):
    ...


class UserOutSchm(BaseModel):
    id: int
    uuid: UUID
    username: str
    full_name: str
    role: str
    is_active: bool
