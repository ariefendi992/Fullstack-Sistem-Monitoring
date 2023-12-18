from typing import Optional, override
from pydantic import BaseModel, ConfigDict


class KelasBase(BaseModel):
    id: Optional[int] = None


class CreateKelasSchema(KelasBase):
    kelas: str


class KelasOutSchema(KelasBase):
    kelas: str

    model_config = ConfigDict(from_attributes=True)
