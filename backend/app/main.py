from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.attendance import router as attendance_router
from app.api.auth import router as auth_router
from app.api.disciplines import router as disciplines_router
from app.api.enrollments import router as enrollments_router
from app.api.health import router as health_router
from app.api.institutions import router as institutions_router
from app.api.students import router as students_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

allow_origins = ["*"] if settings.cors_allow_origins.strip() == "*" else [
    item.strip() for item in settings.cors_allow_origins.split(",") if item.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(institutions_router)
app.include_router(disciplines_router)
app.include_router(students_router)
app.include_router(enrollments_router)
app.include_router(attendance_router)


@app.get("/")
def root() -> dict:
    return {
        "message": "Attend API is running",
        "docs": "/docs",
        "health": "/health",
        "version": settings.app_version,
        "environment": settings.app_env,
        "project_id": settings.gcp_project_id,
    }
