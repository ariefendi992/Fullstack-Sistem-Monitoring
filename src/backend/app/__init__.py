from fastapi import FastAPI
from .core import settings
from app.api import api_router

app = FastAPI(
    title=f"{settings.PROJECT_NAME}",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1-pre",
)


app.include_router(api_router, prefix=f"{settings.API_V1_STR}")
