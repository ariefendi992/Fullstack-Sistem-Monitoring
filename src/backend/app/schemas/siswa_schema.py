from datetime import date
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict
from app.models.user_model import AgamaEnum, GenderEnum
from app.schemas.datums_schema import KelasOutSchema


class SiswaBase(BaseModel):
    gender: GenderEnum
    tempat_lahir: Optional[str]
    tgl_lahir: Optional[date]
    agama: Optional[AgamaEnum]
    nama_ortu: Optional[str]
    alamat: Optional[str]
    telp: Optional[str]


class SiswaCreateSchema(SiswaBase):
    kelas_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateSiswaSchema(SiswaBase):
    kelas_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SiswaOutSchema(SiswaBase):
    qr_name: Optional[str] = None
    photo_name: Optional[str] = None
    idcard_name: Optional[str] = None
    kelas_id: Optional[int] = None
    kelas: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
