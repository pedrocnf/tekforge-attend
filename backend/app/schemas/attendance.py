from datetime import datetime
from pydantic import BaseModel, Field

class AttendanceEventCreate(BaseModel):
    discipline_id: str
    class_id: str
    title: str = Field(min_length=3, max_length=120)
    lesson_date: str = Field(min_length=8, max_length=20)
    lesson_time: str = Field(min_length=3, max_length=20)
    allow_remote_requests: bool = False

class AttendanceEventResponse(BaseModel):
    id: str
    discipline_id: str
    class_id: str
    title: str
    lesson_date: str
    lesson_time: str
    teacher_user_id: str
    allow_remote_requests: bool
    status: str
    created_at: datetime
    closed_at: datetime | None = None

class AttendanceRequestCreate(BaseModel):
    event_id: str
    student_user_id: str
    channel: str = Field(default="web", max_length=20)
    stars: int | None = Field(default=None, ge=1, le=5)
    tags: list[str] = Field(default_factory=list)
    comments: str | None = Field(default=None, max_length=500)

class AttendanceRequestResponse(BaseModel):
    id: str
    event_id: str
    student_user_id: str
    channel: str
    stars: int | None = None
    tags: list[str]
    comments: str | None = None
    status: str
    requested_at: datetime
    reviewed_at: datetime | None = None
    reviewed_by: str | None = None

class AttendanceDecision(BaseModel):
    status: str = Field(pattern="^(confirmed|denied)$")

class AttendanceFinalRecordResponse(BaseModel):
    id: str
    event_id: str
    student_user_id: str
    class_id: str
    discipline_id: str
    status: str
    justification: str | None = None
    updated_at: datetime
