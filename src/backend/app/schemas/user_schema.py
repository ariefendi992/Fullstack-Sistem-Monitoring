from datetime import datetime
from typing import Annotated, Any, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.config import date_to_str, datetime_to_str
from app.schemas.base_schema import EnumRole
from app.schemas.admin_schema import AdminCreateSchm, AdminOutSchema, AdminUpdateSchm
from app.schemas.guru_schema import GuruCreateSchema, GuruOutSchema, GuruUpdateSchema
from app.schemas.siswa_schema import (
    SiswaCreateSchema,
    SiswaOutSchema,
    UpdateSiswaSchema,
)


class UserBase(BaseModel):
    username: str
    password: str


class UserCreateSchm(UserBase):
    full_name: str
    role: EnumRole | None = None
    is_active: bool = True


class UserOutSchm(BaseModel):
    uuid: Annotated[UUID | str, Field(serialization_alias="user_id")]
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: str | datetime
    updated_at: str | datetime
    admin: Optional[AdminOutSchema] = None
    guru: Optional[GuruOutSchema] = None
    siswa: Optional[SiswaOutSchema] = None

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

    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserBase):
    id: int
    admin: list[Any] = []


class CreateUserAdminSchema(UserBase):
    full_name: str = Field(default="John Doe")
    role: EnumRole
    is_active: bool
    admin: AdminCreateSchm | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateAllUserSchema(UserBase):
    full_name: str = Field(default="John Doe")
    role: EnumRole
    is_active: bool
    admin: Optional[AdminCreateSchm] = None
    guru: Optional[GuruCreateSchema] = None
    siswa: Optional[SiswaCreateSchema] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUserSchema(UserBase):
    username: Optional[str] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[EnumRole] = None
    is_active: Optional[bool] = None
    admin: Optional[AdminUpdateSchm] = None
    guru: Optional[GuruUpdateSchema] = None
    siswa: Optional[UpdateSiswaSchema] = None

    model_config = ConfigDict(from_attributes=True)
