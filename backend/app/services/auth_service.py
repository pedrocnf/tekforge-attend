from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, SignupRequest


class AuthService:
    def __init__(self, user_repo: UserRepository | None = None) -> None:
        self.user_repo = user_repo or UserRepository()

    def signup_student(self, payload: SignupRequest) -> dict:
        if self.user_repo.get_by_username(payload.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        if self.user_repo.get_by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

        return self.user_repo.create(
            {
                "username": payload.username.strip().lower(),
                "password_hash": hash_password(payload.password),
                "full_name": payload.full_name.strip(),
                "email": payload.email.strip().lower(),
                "role": "student",
            }
        )

    def login(self, payload: LoginRequest) -> str:
        user = self.user_repo.get_by_username(payload.username.strip().lower())
        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.get("is_active", False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

        return create_access_token(subject=user["id"], extra_claims={"role": user["role"], "username": user["username"]})
