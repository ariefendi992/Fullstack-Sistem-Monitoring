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
    # APP
    SECRET_KEY: str
    PROJECT_NAME: str

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
