from fastapi import APIRouter, HTTPException, status
from app.core.config import settings
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository
router = APIRouter(prefix="/admin", tags=["admin"])
@router.post("/bootstrap")
def bootstrap_admin(password: str) -> dict:
    if not settings.enable_admin_bootstrap:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin bootstrap disabled")
    if password != settings.admin_bootstrap_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bootstrap password")
    repo = UserRepository()
    existing = repo.get_by_username(settings.admin_bootstrap_username)
    if existing:
        return {"status": "already_exists", "username": existing["username"], "role": existing["role"]}
    user = repo.create({"username": settings.admin_bootstrap_username, "password_hash": hash_password(settings.admin_bootstrap_password), "full_name": "TekAttend Admin", "email": settings.admin_bootstrap_email, "role": "admin"})
    return {"status": "created", "user_id": user["id"], "username": user["username"], "role": user["role"]}
