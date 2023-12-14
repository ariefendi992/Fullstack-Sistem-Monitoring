from datetime import date, datetime, timedelta
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
import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    guru = "guru"
    siwsa = "siswa"


class GenderEnum(enum.Enum):
    laki = "laki-laki"
    perempuan = "perempuan"


class AgamaEnum(enum.Enum):
    islam = "islam"
    kristen = "kristen"
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

    def __init__(
        self,
        *,
        username: str,
        hashedPassword: str,
        fullName: str,
        role: str,
        isActive: Boolean = True,
    ):
        self.username = username
        self.hashed_password = hashedPassword
        self.full_name = fullName
        self.role = role
        self.is_active = isActive

    def __repr__(self):
        data = {
            "username": self.username,
            "uuid": self.uuid,
            "full_name": self.full_name,
        }
        return data


class UserLoginModel(Base):
    __tablename__ = "tb_user_login"
    id = Column(Integer, primary_key=True, autoincrement=True)
    refreh_token = Column(String(512), nullable=True)
    user_id = Column(
        Integer, ForeignKey("tb_users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user = relationship("UserModel", backref="user_login")
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
    gender = Column(Enum(GenderEnum), nullable=False)
    agama = Column(Enum(AgamaEnum), nullable=True)
    alamat = Column(String(255), nullable=True)
    telp = Column(String(14), nullable=True)
    user_id = Column(
        Integer, ForeignKey("tb_users.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    user = relationship("UserModel", backref="user_admin")

    def __init__(
        self,
        *,
        userID: str | int,
        gender: str,
        agama: str | None = None,
        alamat: str | None = None,
        telp: str | None = None,
    ):
        self.user_id = (userID,)
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
    user = relationship("UserModel", backref="user_guru")

    def __init__(
        self,
        *,
        userID: int | str,
        gender: str,
        agama: str | None = None,
        alamat: str | None = None,
        telp: str | None = None,
    ):
        self.user_id = userID
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
    user = relationship("UserModel", backref="user_siswa")

    def __init__(
        self,
        *,
        userID: int | str,
        gender: str,
        tempatLahir: str | None = None,
        tglLahir: date | None = None,
        agama: str | None = None,
        namaOrtu: str | None = None,
        alamat: str | None = None,
        telp: str | None = None,
        qrName: str | None = None,
        photoName: str | None = None,
        IDCardName: str | None = None,
        kelasID: int | None = None,
    ):
        self.user_id = userID
        self.gender = gender
        self.tempat_lahir = tempatLahir
        self.tgl_lahir = tglLahir
        self.agama = agama
        self.nama_ortu = namaOrtu
        self.alamat = alamat
        self.telp = telp
        self.qr_name = qrName
        self.photo_name = photoName
        self.idcard_name = IDCardName
        self.kelas_id = kelasID
