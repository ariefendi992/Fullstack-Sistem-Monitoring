from fastapi import FastAPI
from .core import settings
from app.api import api_router

app = FastAPI()


app.include_router(api_router, prefix=f"{settings.API_V1_STR}")
