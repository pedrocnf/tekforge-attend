from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore import Client

from app.core.firestore import get_firestore_client


class ClassRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("classes")

    def list_all(self) -> list[dict[str, Any]]:
        docs = self.collection.order_by("name").stream()
        items: list[dict[str, Any]] = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(data)
        return items

    def get_by_id(self, class_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(class_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc_ref = self.collection.document()
        record = {
            "name": payload["name"],
            "semester": payload["semester"],
            "shift": payload.get("shift"),
            "is_active": True,
            "created_at": now,
        }
        doc_ref.set(record)
        record["id"] = doc_ref.id
        return record
