from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, DateTime, Enum, Integer, String, func
from app.db.engine import Base


class UserModel(Base):
    __tablename__ = "tb_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, nullable=False, default=uuid4)
    username = Column(String(32), nullable=False)
    hashed_password = Column(String, nullable=False)
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
