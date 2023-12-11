from datetime import datetime
from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import engine, Base
from app.db.engine import SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash


async def get_db() -> Generator:
    db = SessionLocal()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield db
    finally:
        await db.close()


SessionDepends = Annotated[AsyncSession, Depends(get_db)]


# NOTE: generate password_hash
def gen_password_hash(password: str) -> Generator:
    return generate_password_hash(password)


# NOTE: check_pasword_hash
def password_hash_check(password, password_hash):
    return check_password_hash(pwhash=password_hash, password=password)


WEEKDAYLIST: list[str] = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
MONTHLIST: list[str] = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]


# Date convertion to String
def date_to_str(datetime: datetime):
    hari = WEEKDAYLIST[datetime.weekday()]
    tgl: int = datetime.day
    bulan = MONTHLIST[datetime.month - 1]
    tahun: int = datetime.year

    return f"{hari}-{tgl}-{bulan}-{tahun}"


# Date time convertion to String
def datetime_to_str(datetime: datetime):
    hari = WEEKDAYLIST[datetime.weekday()]
    tgl: int = datetime.day
    bulan = MONTHLIST[datetime.month - 1]
    tahun: int = datetime.year

    jam = datetime.hour if len(str(datetime.hour)) > 1 else f"0{datetime.hour}"
    menit = datetime.minute
    detik = datetime.second
    return f"{hari}-{tgl}-{bulan}-{tahun} | {jam}:{menit}:{detik}"
