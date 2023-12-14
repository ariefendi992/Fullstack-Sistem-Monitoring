from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from app.db.engine import Base
from app.core import settings


class UserModel(Base):
    __tablename__ = "tb_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, nullable=False, default=uuid4)
    username = Column(String(32), nullable=False, unique=True)
    hashed_password = Column(String(512), nullable=False)
    full_name = Column(String(64), nullable=False)
    role = Column(Enum("admin", "guru", "siswa"), nullable=False)
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
        isActive: Boolean = True
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
