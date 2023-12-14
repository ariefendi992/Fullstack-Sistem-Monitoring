from datetime import datetime
from typing import Annotated, Any, Optional, Dict
from pydantic import MySQLDsn, ValidationInfo, field_validator, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    # APP & SECURITY
    SECRET_KEY: str
    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    EXPIRE_TIMEDELTA_MINUTE: int = 30
    # menit * jam * hari = 7 hari
    REFRESH_EXPIRE_TIMEDETLA_MINUTE: int = 60 * 24 * 7

    # MySQL
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    SQLALCHEMY_DATABASE_URI: Optional[MySQLDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str, info: ValidationInfo):
        if isinstance(v, str):
            return v
        data = info.data
        return MySQLDsn.build(
            scheme="mysql+aiomysql",
            username=data.get("DB_USER"),
            password=data.get("DB_PASSWORD"),
            host=data.get("DB_HOST"),
            path=data.get("DB_NAME"),
        )


@lru_cache
def get_settings():
    return Settings()


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
