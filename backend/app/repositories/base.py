from datetime import datetime, timezone
from google.cloud.firestore import Client
from app.core.firestore import get_firestore_client

class BaseRepository:
    collection_name: str = ""
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection(self.collection_name)
    def get_by_id(self, doc_id: str):
        doc = self.collection.document(doc_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict(); data["id"] = doc.id
        return data
    def create(self, payload: dict):
        ref = self.collection.document()
        payload.setdefault("created_at", datetime.now(timezone.utc))
        ref.set(payload)
        payload["id"] = ref.id
        return payload
