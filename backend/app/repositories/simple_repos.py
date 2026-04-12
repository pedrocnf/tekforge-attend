from datetime import datetime, timezone
from app.repositories.base import BaseRepository

class InstitutionRepository(BaseRepository):
    collection_name = "institutions"
    def list_all(self):
        out=[]
        for doc in self.collection.order_by("name").stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out
    def update(self, doc_id: str, payload: dict):
        self.collection.document(doc_id).update(payload)
        return self.get_by_id(doc_id)

class DisciplineRepository(BaseRepository):
    collection_name = "disciplines"
    def list_all(self):
        out=[]
        for doc in self.collection.order_by("name").stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out

class StudentRepository(BaseRepository):
    collection_name = "students"
    def create(self, payload: dict):
        return super().create({
            "user_id": payload["user_id"], "full_name": payload["full_name"], "class_name": payload["class_name"],
            "cpf": payload["cpf"], "email": payload["email"], "phone": payload["phone"],
            "created_by_user_id": payload.get("created_by_user_id"), "created_at": datetime.now(timezone.utc)
        })
    def list_all(self):
        out=[]
        for doc in self.collection.order_by("full_name").stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out
    def get_by_user_id(self, user_id: str):
        docs=list(self.collection.where("user_id","==",user_id).limit(1).stream())
        if not docs: return None
        d=docs[0].to_dict(); d["id"]=docs[0].id; return d
    def update(self, doc_id: str, payload: dict):
        self.collection.document(doc_id).update(payload)
        return self.get_by_id(doc_id)

class EnrollmentRepository(BaseRepository):
    collection_name = "enrollments"
    def create(self, payload: dict):
        return super().create({"student_user_id": payload["student_user_id"], "discipline_id": payload["discipline_id"], "is_active": True, "created_at": datetime.now(timezone.utc)})
    def list_all(self):
        out=[]
        for doc in self.collection.order_by("created_at").stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out
    def find_active(self, student_user_id: str, discipline_id: str):
        docs=list(self.collection.where("student_user_id","==",student_user_id).where("discipline_id","==",discipline_id).where("is_active","==",True).limit(1).stream())
        if not docs: return None
        d=docs[0].to_dict(); d["id"]=docs[0].id; return d
    def list_by_discipline(self, discipline_id: str):
        out=[]
        for doc in self.collection.where("discipline_id","==",discipline_id).where("is_active","==",True).stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out

class VerificationTokenRepository(BaseRepository):
    collection_name = "verification_tokens"
    def create_token(self, user_id: str, token: str, purpose: str):
        return super().create({"user_id": user_id, "token": token, "purpose": purpose, "used": False, "created_at": datetime.now(timezone.utc)})
    def get_valid_token(self, token: str, purpose: str):
        docs=list(self.collection.where("token","==",token).where("purpose","==",purpose).where("used","==",False).limit(1).stream())
        if not docs: return None
        d=docs[0].to_dict(); d["id"]=docs[0].id; return d
    def mark_used(self, token_id: str):
        self.collection.document(token_id).update({"used": True})

class AttendanceEventRepository(BaseRepository):
    collection_name = "attendance_events"
    def create(self, payload: dict):
        return super().create({"discipline_id": payload["discipline_id"], "title": payload["title"], "lesson_date": payload["lesson_date"], "lesson_time": payload["lesson_time"], "teacher_user_id": payload["teacher_user_id"], "allow_remote_requests": payload["allow_remote_requests"], "status": "open", "closed_at": None, "created_at": datetime.now(timezone.utc)})
    def list_all(self):
        out=[]
        for doc in self.collection.order_by("created_at", direction="DESCENDING").stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out
    def close(self, event_id: str):
        self.collection.document(event_id).update({"status": "closed", "closed_at": datetime.now(timezone.utc)})

class AttendanceRequestRepository(BaseRepository):
    collection_name = "attendance_requests"
    def create(self, payload: dict):
        return super().create({"event_id": payload["event_id"], "student_user_id": payload["student_user_id"], "channel": payload["channel"], "stars": payload.get("stars"), "tags": payload.get("tags", []), "comments": payload.get("comments"), "status": "pending", "requested_at": datetime.now(timezone.utc), "reviewed_at": None, "reviewed_by": None, "created_at": datetime.now(timezone.utc)})
    def find_existing_pending(self, event_id: str, student_user_id: str):
        docs=list(self.collection.where("event_id","==",event_id).where("student_user_id","==",student_user_id).where("status","==","pending").limit(1).stream())
        if not docs: return None
        d=docs[0].to_dict(); d["id"]=docs[0].id; return d
    def list_by_event(self, event_id: str):
        out=[]
        for doc in self.collection.where("event_id","==",event_id).stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        out.sort(key=lambda x: str(x.get("requested_at")))
        return out
    def review(self, request_id: str, status: str, reviewed_by: str):
        self.collection.document(request_id).update({"status": status, "reviewed_at": datetime.now(timezone.utc), "reviewed_by": reviewed_by})

class AttendanceFinalRecordRepository(BaseRepository):
    collection_name = "attendance_final_records"
    def upsert(self, event_id: str, student_user_id: str, payload: dict):
        docs=list(self.collection.where("event_id","==",event_id).where("student_user_id","==",student_user_id).limit(1).stream())
        rec={"event_id": event_id, "student_user_id": student_user_id, "discipline_id": payload["discipline_id"], "status": payload["status"], "justification": payload.get("justification"), "updated_at": datetime.now(timezone.utc), "created_at": datetime.now(timezone.utc)}
        if docs:
            self.collection.document(docs[0].id).set(rec)
            rec["id"]=docs[0].id
            return rec
        return super().create(rec)
    def list_by_event(self, event_id: str):
        out=[]
        for doc in self.collection.where("event_id","==",event_id).stream():
            d=doc.to_dict(); d["id"]=doc.id; out.append(d)
        return out
