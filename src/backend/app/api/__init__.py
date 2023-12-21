from fastapi import APIRouter
from .endpoints_v1 import user_api, login_api, datum_api

api_router = APIRouter()
api_router.include_router(login_api.router, prefix='/auth', tags=["Auth"])
api_router.include_router(
    user_api.router, prefix="/users", tags=["Users (Only admins can access this)"]
)

api_router.include_router(datum_api.router, prefix="/data-umum", tags=["Data Umum"])
