from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.config import settings
from app.core.exceptions import AppException
from app.core.middleware import RequestLoggingMiddleware
from app.tasks.activity_scheduler import activity_scheduler_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with activity_scheduler_lifespan():
        yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs" if settings.app_debug else None,
    redoc_url="/redoc" if settings.app_debug else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)


@app.exception_handler(AppException)
async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "detail": exc.detail},
    )


@app.get("/health")
async def health_check() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.app_env,
    }


app.include_router(api_router, prefix="/api/v1")
