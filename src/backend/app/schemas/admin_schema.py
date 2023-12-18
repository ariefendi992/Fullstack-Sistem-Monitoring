from typing import Optional
from pydantic import BaseModel
from app.models.user_model import AgamaEnum, GenderEnum


class AdminBase(BaseModel):
    gender: Optional[GenderEnum]
    agama: Optional[AgamaEnum]
    alamat: Optional[str]
    telp: Optional[str]


class AdminCreateSchm(AdminBase):
    ...


class AdminUpdateSchm(AdminBase):
    ...


class AdminSchema(AdminBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class AdminOutSchema(AdminBase):
    ...
