from fastapi import HTTPException, status
from app.repositories.attendance_repository import AttendanceEventRepository, AttendanceFinalRecordRepository, AttendanceRequestRepository
from app.repositories.class_repository import ClassRepository
from app.repositories.discipline_repository import DisciplineRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.attendance import AttendanceEventCreate, AttendanceRequestCreate

class AttendanceService:
    def __init__(self) -> None:
        self.events = AttendanceEventRepository()
        self.requests = AttendanceRequestRepository()
        self.records = AttendanceFinalRecordRepository()
        self.classes = ClassRepository()
        self.disciplines = DisciplineRepository()
        self.enrollments = EnrollmentRepository()
        self.users = UserRepository()

    def create_event(self, payload: AttendanceEventCreate, actor: dict) -> dict:
        if not self.classes.get_by_id(payload.class_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
        if not self.disciplines.get_by_id(payload.discipline_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discipline not found")
        return self.events.create({"discipline_id": payload.discipline_id, "class_id": payload.class_id, "title": payload.title.strip(), "lesson_date": payload.lesson_date.strip(), "lesson_time": payload.lesson_time.strip(), "teacher_user_id": actor["id"], "allow_remote_requests": payload.allow_remote_requests})

    def list_events(self) -> list[dict]:
        return self.events.list_all()

    def create_request(self, payload: AttendanceRequestCreate) -> dict:
        event = self.events.get_by_id(payload.event_id)
        if not event: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        if event["status"] != "open": raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event is closed")
        student = self.users.get_by_id(payload.student_user_id)
        if not student or student["role"] != "student": raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not found")
        if not self.enrollments.find_active(payload.student_user_id, event["class_id"], event["discipline_id"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student is not enrolled in this class and discipline")
        if self.requests.find_existing_pending(payload.event_id, payload.student_user_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pending request already exists")
        return self.requests.create({"event_id": payload.event_id, "student_user_id": payload.student_user_id, "channel": payload.channel, "stars": payload.stars, "tags": payload.tags, "comments": payload.comments})

    def list_requests(self, event_id: str) -> list[dict]:
        return self.requests.list_by_event(event_id)

    def review_request(self, request_id: str, status_value: str, actor: dict) -> dict:
        request = self.requests.get_by_id(request_id)
        if not request: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        event = self.events.get_by_id(request["event_id"])
        if not event: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        self.requests.review(request_id, status_value, actor["id"])
        final_status = "confirmed" if status_value == "confirmed" else "unconfirmed"
        record = self.records.upsert(event["id"], request["student_user_id"], {"class_id": event["class_id"], "discipline_id": event["discipline_id"], "status": final_status, "justification": None})
        request["status"] = status_value; request["reviewed_by"] = actor["id"]
        return {"request": request, "record": record}

    def close_event(self, event_id: str) -> dict:
        event = self.events.get_by_id(event_id)
        if not event: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
        enrollments = self.enrollments.list_by_event_scope(event["class_id"], event["discipline_id"])
        existing = {r["student_user_id"]: r for r in self.records.list_by_event(event_id)}
        for enr in enrollments:
            if enr["student_user_id"] not in existing:
                self.records.upsert(event_id, enr["student_user_id"], {"class_id": event["class_id"], "discipline_id": event["discipline_id"], "status": "absent", "justification": None})
        self.events.close(event_id)
        event["status"] = "closed"
        return event

    def list_final_records(self, event_id: str) -> list[dict]:
        return self.records.list_by_event(event_id)
