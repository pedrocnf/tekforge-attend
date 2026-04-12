from datetime import datetime, timezone
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    collection_name = "users"
    def get_by_username(self, username: str):
        docs = list(self.collection.where("username", "==", username).limit(1).stream())
        if not docs: return None
        d = docs[0].to_dict(); d["id"] = docs[0].id
        return d
    def get_by_email(self, email: str):
        docs = list(self.collection.where("email", "==", email).limit(1).stream())
        if not docs: return None
        d = docs[0].to_dict(); d["id"] = docs[0].id
        return d
    def create(self, payload: dict):
        payload = {
            "username": payload["username"],
            "password_hash": payload["password_hash"],
            "full_name": payload["full_name"],
            "email": payload["email"],
            "role": payload["role"],
            "is_active": True,
            "is_email_verified": payload.get("is_email_verified", False),
            "created_at": datetime.now(timezone.utc),
        }
        return super().create(payload)
    def update_role(self, user_id: str, role: str) -> None:
        self.collection.document(user_id).update({"role": role})
    def verify_email(self, user_id: str) -> None:
        self.collection.document(user_id).update({"is_email_verified": True})
    def update_password(self, user_id: str, password_hash: str) -> None:
        self.collection.document(user_id).update({"password_hash": password_hash, "is_email_verified": False})
