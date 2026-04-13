from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

allow_origins = ["*"]
if hasattr(settings, "cors_allow_origins"):
    raw = str(settings.cors_allow_origins).strip()
    if raw and raw != "*":
        allow_origins = [item.strip() for item in raw.split(",") if item.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root() -> dict:
    return {
        "message": "Attend API is running",
        "docs": "/docs",
        "health": "/health",
        "version": settings.app_version,
        "environment": settings.app_env,
    }