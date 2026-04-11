from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore import Client

from app.core.firestore import get_firestore_client


class TeacherRoleRequestRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("teacher_role_requests")

    def get_pending_for_user(self, user_id: str) -> dict[str, Any] | None:
        docs = list(
            self.collection.where("user_id", "==", user_id).where("status", "==", "pending").limit(1).stream()
        )
        if not docs:
            return None
        data = docs[0].to_dict()
        data["id"] = docs[0].id
        return data

    def create(self, user: dict[str, Any], justification: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc_ref = self.collection.document()
        record = {
            "user_id": user["id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "email": user["email"],
            "status": "pending",
            "justification": justification,
            "requested_at": now,
            "reviewed_at": None,
            "reviewed_by": None,
        }
        doc_ref.set(record)
        record["id"] = doc_ref.id
        return record

    def list_pending(self) -> list[dict[str, Any]]:
        docs = self.collection.where("status", "==", "pending").stream()
        results: list[dict[str, Any]] = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        return sorted(results, key=lambda x: x["requested_at"])

    def get_by_id(self, request_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(request_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    def review(self, request_id: str, status: str, reviewed_by: str) -> None:
        self.collection.document(request_id).update(
            {
                "status": status,
                "reviewed_at": datetime.now(timezone.utc),
                "reviewed_by": reviewed_by,
            }
        )
