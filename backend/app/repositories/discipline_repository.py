from datetime import datetime, timezone
from typing import Any
from google.cloud.firestore import Client
from app.core.firestore import get_firestore_client

class DisciplineRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("disciplines")

    def list_all(self) -> list[dict[str, Any]]:
        out = []
        for doc in self.collection.order_by("name").stream():
            d = doc.to_dict(); d["id"] = doc.id; out.append(d)
        return out

    def get_by_id(self, discipline_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(discipline_id).get()
        if not doc.exists: return None
        d = doc.to_dict(); d["id"] = doc.id; return d

    def get_by_code(self, code: str) -> dict[str, Any] | None:
        docs = list(self.collection.where("code", "==", code).limit(1).stream())
        if not docs: return None
        d = docs[0].to_dict(); d["id"] = docs[0].id; return d

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        ref = self.collection.document()
        record = {"name": payload["name"], "code": payload["code"], "description": payload.get("description"), "is_active": True, "created_at": now}
        ref.set(record); record["id"] = ref.id; return record
