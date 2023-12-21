from datetime import datetime, timedelta
from typing import Generator
from jose import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.core import settings


# NOTE: generate password_hash
def gen_password_hash(password: str) -> Generator:
    return generate_password_hash(password)


# NOTE: check_pasword_hash
def password_hash_check(password, password_hash):
    return check_password_hash(pwhash=password_hash, password=password)


ALGORITHM = "HS256"


def create_access_token(*, identity: str | dict, expire_delta: timedelta = None):
    if expire_delta:
        expire = datetime.now() + expire_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.EXPIRE_TIMEDELTA_MINUTE)

    if isinstance(identity, str):
        to_encode = {"exp": expire, "identity": identity}
        jwt_encode = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(identity, dict):
        to_encode = {"exp": expire, "identity": identity}
        jwt_encode = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encode


def create_refresh_token(*, identity: str | dict, expire_delta: timedelta = None):
    expire = (
        datetime.now() + expire_delta
        if expire_delta
        else datetime.now() + timedelta(minutes=settings.EXPIRE_TIMEDELTA_MINUTE)
    )

    if isinstance(identity, str):
        to_encode = {"exp": expire, "identity": identity}
        jwt_encode = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    if isinstance(identity, dict):
        to_encode = {"exp": expire, "identity": identity}
        jwt_encode = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encode
