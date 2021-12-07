"""
Main FastAPI app instance declaration
"""
from time import time
from typing import Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/v1")


@app.middleware("http")  # type: ignore
async def add_process_time_header(request: Request, call_next: Any):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response
