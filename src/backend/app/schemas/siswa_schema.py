from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models.user_model import AgamaEnum, GenderEnum


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
