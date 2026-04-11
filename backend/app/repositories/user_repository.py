from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore import Client

from app.core.firestore import get_firestore_client


class UserRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("users")

    def get_by_username(self, username: str) -> dict[str, Any] | None:
        docs = list(self.collection.where("username", "==", username).limit(1).stream())
        if not docs:
            return None
        data = docs[0].to_dict()
        data["id"] = docs[0].id
        return data

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        docs = list(self.collection.where("email", "==", email).limit(1).stream())
        if not docs:
            return None
        data = docs[0].to_dict()
        data["id"] = docs[0].id
        return data

    def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(user_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc_ref = self.collection.document()
        record = {
            "username": payload["username"],
            "password_hash": payload["password_hash"],
            "full_name": payload["full_name"],
            "email": payload["email"],
            "role": payload["role"],
            "is_active": True,
            "created_at": now,
        }
        doc_ref.set(record)
        record["id"] = doc_ref.id
        return record

    def update_role(self, user_id: str, role: str) -> None:
        self.collection.document(user_id).update({"role": role})
