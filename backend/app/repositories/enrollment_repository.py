from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore import Client

from app.core.firestore import get_firestore_client


class EnrollmentRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("enrollments")

    def list_all(self) -> list[dict[str, Any]]:
        docs = self.collection.order_by("created_at").stream()
        items: list[dict[str, Any]] = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(data)
        return items

    def find_active(self, student_user_id: str, class_id: str, discipline_id: str) -> dict[str, Any] | None:
        docs = list(
            self.collection.where("student_user_id", "==", student_user_id)
            .where("class_id", "==", class_id)
            .where("discipline_id", "==", discipline_id)
            .where("is_active", "==", True)
            .limit(1)
            .stream()
        )
        if not docs:
            return None
        data = docs[0].to_dict()
        data["id"] = docs[0].id
        return data

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc_ref = self.collection.document()
        record = {
            "student_user_id": payload["student_user_id"],
            "class_id": payload["class_id"],
            "discipline_id": payload["discipline_id"],
            "is_active": True,
            "created_at": now,
        }
        doc_ref.set(record)
        record["id"] = doc_ref.id
        return record
