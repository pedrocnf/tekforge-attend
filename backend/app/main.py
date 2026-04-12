from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.academic import router as academic_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.teacher_role_requests import router as teacher_role_requests_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(teacher_role_requests_router)
app.include_router(admin_router)
app.include_router(academic_router)


@app.get("/")
def root() -> dict:
    return {
        "message": "TekAttend API is running",
        "docs": "/docs",
        "health": "/health",
        "version": settings.app_version,
    }
