from fastapi import APIRouter
from app.core.config import settings
router = APIRouter(tags=["health"])
@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version, "environment": settings.app_env}
