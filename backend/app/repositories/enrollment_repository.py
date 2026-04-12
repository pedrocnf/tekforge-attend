from datetime import datetime, timezone
from typing import Any
from google.cloud.firestore import Client
from app.core.firestore import get_firestore_client

class EnrollmentRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("enrollments")

    def list_all(self) -> list[dict[str, Any]]:
        out = []
        for doc in self.collection.order_by("created_at").stream():
            d = doc.to_dict(); d["id"] = doc.id; out.append(d)
        return out

    def find_active(self, student_user_id: str, class_id: str, discipline_id: str) -> dict[str, Any] | None:
        docs = list(self.collection.where("student_user_id", "==", student_user_id).where("class_id", "==", class_id).where("discipline_id", "==", discipline_id).where("is_active", "==", True).limit(1).stream())
        if not docs: return None
        d = docs[0].to_dict(); d["id"] = docs[0].id; return d

    def list_by_event_scope(self, class_id: str, discipline_id: str) -> list[dict[str, Any]]:
        out = []
        for doc in self.collection.where("class_id", "==", class_id).where("discipline_id", "==", discipline_id).where("is_active", "==", True).stream():
            d = doc.to_dict(); d["id"] = doc.id; out.append(d)
        return out

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        ref = self.collection.document()
        record = {"student_user_id": payload["student_user_id"], "class_id": payload["class_id"], "discipline_id": payload["discipline_id"], "is_active": True, "created_at": now}
        ref.set(record); record["id"] = ref.id; return record
