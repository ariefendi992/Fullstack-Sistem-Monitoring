from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .core import settings
from app.api import api_router


app = FastAPI(
    title=f"{settings.PROJECT_NAME}",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1-pre",
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=f"{settings.API_V1_STR}")
