from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.engine import Base


class KelasModel(Base):
    __tablename__ = "tb_datum_kelas"
    id = Column(Integer, primary_key=True)
    kelas = Column(String(16), nullable=False, unique=True)
    siswa = relationship("UserDetailSiswa", back_populates="kelas")

    def __init__(self, *, kelas: str) -> str:
        self.kelas = kelas

    def __repr__(self) -> str:
        return self.kelas
