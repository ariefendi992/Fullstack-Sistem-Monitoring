from typing import Annotated
from uuid import UUID
from pydantic import BaseModel


class TokenShema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayloadSchema(BaseModel):
    # identity: dict[str, Any] | str | None = None
    username: str | None = None
    user_id: str | None = None
    scopes: list[str] = []
