from datetime import datetime, timezone
from typing import Any

from google.cloud.firestore import Client

from app.core.firestore import get_firestore_client


class DisciplineRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("disciplines")

    def list_all(self) -> list[dict[str, Any]]:
        docs = self.collection.order_by("name").stream()
        items: list[dict[str, Any]] = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            items.append(data)
        return items

    def get_by_id(self, discipline_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(discipline_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    def get_by_code(self, code: str) -> dict[str, Any] | None:
        docs = list(self.collection.where("code", "==", code).limit(1).stream())
        if not docs:
            return None
        data = docs[0].to_dict()
        data["id"] = docs[0].id
        return data

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        doc_ref = self.collection.document()
        record = {
            "name": payload["name"],
            "code": payload["code"],
            "description": payload.get("description"),
            "is_active": True,
            "created_at": now,
        }
        doc_ref.set(record)
        record["id"] = doc_ref.id
        return record
