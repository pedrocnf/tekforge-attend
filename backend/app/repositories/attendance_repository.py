from datetime import datetime, timezone
from typing import Any
from google.cloud.firestore import Client
from app.core.firestore import get_firestore_client

class AttendanceEventRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("attendance_events")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        ref = self.collection.document()
        record = {"discipline_id": payload["discipline_id"], "class_id": payload["class_id"], "title": payload["title"], "lesson_date": payload["lesson_date"], "lesson_time": payload["lesson_time"], "teacher_user_id": payload["teacher_user_id"], "allow_remote_requests": payload["allow_remote_requests"], "status": "open", "created_at": now, "closed_at": None}
        ref.set(record); record["id"] = ref.id; return record

    def get_by_id(self, event_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(event_id).get()
        if not doc.exists: return None
        d = doc.to_dict(); d["id"] = doc.id; return d

    def list_all(self) -> list[dict[str, Any]]:
        out = []
        for doc in self.collection.order_by("created_at", direction="DESCENDING").stream():
            d = doc.to_dict(); d["id"] = doc.id; out.append(d)
        return out

    def close(self, event_id: str) -> None:
        self.collection.document(event_id).update({"status": "closed", "closed_at": datetime.now(timezone.utc)})

class AttendanceRequestRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("attendance_requests")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        ref = self.collection.document()
        record = {"event_id": payload["event_id"], "student_user_id": payload["student_user_id"], "channel": payload["channel"], "stars": payload.get("stars"), "tags": payload.get("tags", []), "comments": payload.get("comments"), "status": "pending", "requested_at": now, "reviewed_at": None, "reviewed_by": None}
        ref.set(record); record["id"] = ref.id; return record

    def find_existing_pending(self, event_id: str, student_user_id: str) -> dict[str, Any] | None:
        docs = list(self.collection.where("event_id", "==", event_id).where("student_user_id", "==", student_user_id).where("status", "==", "pending").limit(1).stream())
        if not docs: return None
        d = docs[0].to_dict(); d["id"] = docs[0].id; return d

    def list_by_event(self, event_id: str) -> list[dict[str, Any]]:
        out = []
        for doc in self.collection.where("event_id", "==", event_id).order_by("requested_at").stream():
            d = doc.to_dict(); d["id"] = doc.id; out.append(d)
        return out

    def get_by_id(self, request_id: str) -> dict[str, Any] | None:
        doc = self.collection.document(request_id).get()
        if not doc.exists: return None
        d = doc.to_dict(); d["id"] = doc.id; return d

    def review(self, request_id: str, status: str, reviewed_by: str) -> None:
        self.collection.document(request_id).update({"status": status, "reviewed_at": datetime.now(timezone.utc), "reviewed_by": reviewed_by})

class AttendanceFinalRecordRepository:
    def __init__(self, client: Client | None = None) -> None:
        self.client = client or get_firestore_client()
        self.collection = self.client.collection("attendance_final_records")

    def upsert(self, event_id: str, student_user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        docs = list(self.collection.where("event_id", "==", event_id).where("student_user_id", "==", student_user_id).limit(1).stream())
        record = {"event_id": event_id, "student_user_id": student_user_id, "class_id": payload["class_id"], "discipline_id": payload["discipline_id"], "status": payload["status"], "justification": payload.get("justification"), "updated_at": datetime.now(timezone.utc)}
        if docs:
            ref = self.collection.document(docs[0].id)
            ref.set(record)
            record["id"] = docs[0].id
        else:
            ref = self.collection.document(); ref.set(record); record["id"] = ref.id
        return record

    def list_by_event(self, event_id: str) -> list[dict[str, Any]]:
        out = []
        for doc in self.collection.where("event_id", "==", event_id).stream():
            d = doc.to_dict(); d["id"] = doc.id; out.append(d)
        return out
