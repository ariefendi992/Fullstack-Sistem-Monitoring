from fastapi import APIRouter
from .endpoints_v1 import user_api, login_api

api_router = APIRouter()
api_router.include_router(login_api.router, tags=["Login"])
api_router.include_router(
    user_api.router, prefix="/users", tags=["Users (Only admins can access this)"]
)
