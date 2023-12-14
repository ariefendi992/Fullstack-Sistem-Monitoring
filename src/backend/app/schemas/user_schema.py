from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Optional
from uuid import UUID
from pydantic import BaseModel, Field, field_validator

from app.core.config import date_to_str, datetime_to_str


class EnumRole(str, Enum):
    admin: str = "admin"
    guru: str = "guru"
    siswa: str = "siswa"


class UserBase(BaseModel):
    username: str
    password: str = Field(..., exclude=True)


class UserCreateSchm(UserBase):
    full_name: str
    role: EnumRole
    is_active: bool = True


class UserUpdateSchm(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[EnumRole] = None
    is_active: Optional[bool] = None


class UserOutSchm(BaseModel):
    uuid: Annotated[UUID | str, Field(serialization_alias="user_id")]
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: str | datetime
    # updated_at: str | datetime
    updated_at: str | datetime

    @field_validator("created_at")
    @classmethod
    def assemble_date_str(cls, v: Any):
        if isinstance(v, datetime):
            return date_to_str(v)

    @field_validator("updated_at")
    @classmethod
    def assemble_datetime_str(cls, v: Any):
        if isinstance(v, datetime):
            return f"{datetime_to_str(v)}"
