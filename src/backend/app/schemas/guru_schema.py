from typing import Optional
from pydantic import BaseModel
from app.models.user_model import AgamaEnum, GenderEnum


class GuruBase(BaseModel):
    gender: Optional[GenderEnum]
    agama: Optional[AgamaEnum]
    alamat: Optional[str]
    telp: Optional[str]


class GuruCreateSchema(GuruBase):
    ...


class GuruUpdateSchema(GuruBase):
    ...


class GuruOutSchema(GuruBase):
    ...
