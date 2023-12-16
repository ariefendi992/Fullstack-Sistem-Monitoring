from datetime import date, datetime, timedelta
from typing import Optional
from uuid import uuid4
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship
from app.db.engine import Base
from app.core import settings
from app.schemas.base_schema import EnumRole
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    guru = "guru"
    siwsa = "siswa"


class GenderEnum(str, enum.Enum):
    laki = "laki-laki"
    perempuan = "perempuan"


class AgamaEnum(str, enum.Enum):
    islam = "islam"
    kristen = "kristen"
    katolik = "katolik"
    hindu = "hindu"
    budha = "budha"
    konghucu = "konghucu"


class UserModel(Base):
    __tablename__ = "tb_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, nullable=False, default=uuid4)
    username = Column(String(32), nullable=False, unique=True)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(64), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    login = relationship("UserLoginModel", back_populates="user")
    admin = relationship("UserDetailAdmin", back_populates="user")
    guru = relationship("UserDetailGuru", back_populates="user")
    siswa = relationship("UserDetailSiswa", back_populates="user")

    def __init__(
        self,
        username: str,
        hashedPassword: str,
        full_name: str,
        role: EnumRole,
        is_active: Boolean = True,
        admin: Optional["UserDetailAdmin"] = [],
        guru: Optional["UserDetailGuru"] = [],
        siswa: Optional["UserDetailSiswa"] = [],
    ):
        self.username = username
        self.hashed_password = hashedPassword
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.admin = admin
        self.guru = guru
        self.siswa = siswa

    def __repr__(self):
        data = (f"username : {self.username}",)

        return data


class UserLoginModel(Base):
    __tablename__ = "tb_user_login"
    id = Column(Integer, primary_key=True, autoincrement=True)
    refreh_token = Column(String(512), nullable=True)
    user_id = Column(
        Integer, ForeignKey("tb_users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user = relationship("UserModel", back_populates="login")
    expire_token = Column(DateTime, nullable=False)
    counter_login = Column(Integer, nullable=False, default=0)
    last_login_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, *, refrehToken, userID, expireDelta: timedelta | None = None):
        self.refreh_token = refrehToken
        self.user_id = userID
        self.counter_login: int = +1
        if expireDelta:
            self.expire_token = datetime.now() + expireDelta
        else:
            self.expire_token = datetime.now() + timedelta(
                minutes=settings.REFRESH_EXPIRE_TIMEDETLA_MINUTE
            )


class UserDetailAdmin(Base):
    __tablename__ = "tb_detail_admin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(Enum("laki-laki", "perempuan"), nullable=False)
    agama = Column(Enum(AgamaEnum), nullable=True)
    alamat = Column(String(255), nullable=True)
    telp = Column(String(14), nullable=True)
    user_id = Column(
        Integer, ForeignKey("tb_users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user = relationship("UserModel", back_populates="admin")

    def __init__(
        self,
        *,
        gender: str,
        agama: str | None = None,
        alamat: str | None = None,
        telp: str | None = None,
    ):
        self.gender = gender
        self.agama = agama
        self.alamat = alamat
        self.telp = telp


class UserDetailGuru(Base):
    __tablename__ = "tb_detail_guru"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    agama = Column(Enum(AgamaEnum), nullable=True)
    alamat = Column(String(255), nullable=True)
    telp = Column(String(14), nullable=True)
    user_id = Column(
        Integer, ForeignKey("tb_users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user = relationship("UserModel", back_populates="guru")

    def __init__(
        self,
        *,
        gender: str,
        agama: str | None = None,
        alamat: str | None = None,
        telp: str | None = None,
    ):
        self.gender = gender
        self.agama = agama
        self.alamat = alamat
        self.telp = telp


class UserDetailSiswa(Base):
    __tablename__ = "tb_detail_siswa"
    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    tempat_lahir = Column(String(64), nullable=True)
    tgl_lahir = Column(Date, nullable=True)
    agama = Column(Enum(AgamaEnum), nullable=True)
    nama_ortu = Column(String(64), nullable=True)
    alamat = Column(String(255), nullable=True)
    telp = Column(String(14), nullable=True)
    qr_name = Column(String(255), nullable=True)
    photo_name = Column(String(255), nullable=True)
    idcard_name = Column(String(255), nullable=True)
    kelas_id = Column(Integer, nullable=True)
    user_id = Column(
        Integer, ForeignKey("tb_users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user = relationship("UserModel", back_populates="siswa")

    def __init__(
        self,
        *,
        gender: str,
        tempat_lahir: str | None = None,
        tgl_lahir: date | None = None,
        agama: str | None = None,
        nama_ortu: str | None = None,
        alamat: str | None = None,
        telp: str | None = None,
        qr_name: str | None = None,
        photo_name: str | None = None,
        id_card_name: str | None = None,
        kelas_id: int | None = None,
    ):
        self.gender = gender
        self.tempat_lahir = tempat_lahir
        self.tgl_lahir = tgl_lahir
        self.agama = agama
        self.nama_ortu = nama_ortu
        self.alamat = alamat
        self.telp = telp
        self.qr_name = qr_name
        self.photo_name = photo_name
        self.idcard_name = id_card_name
        self.kelas_id = kelas_id
