from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    cpf: str | None = None
    phone: str | None = None
    class_name: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class FirstAccessRequest(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=6, max_length=128)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    role: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime

class InstitutionCreate(BaseModel):
    name: str
    cep: str
    street: str
    number: str
    complement: str | None = None
    district: str
    city: str
    state: str

class InstitutionResponse(InstitutionCreate):
    id: str
    is_active: bool
    created_at: datetime

class WeeklyMeeting(BaseModel):
    weekday: str
    start_time: str
    end_time: str

class DisciplineCreate(BaseModel):
    name: str
    institution_id: str
    semester: str
    academic_shift: str
    period_label: str
    weekly_meetings: list[WeeklyMeeting]
    total_workload_hours: float
    weekly_lessons_count: int
    lesson_duration_minutes: int

class DisciplineResponse(DisciplineCreate):
    id: str
    is_active: bool
    created_at: datetime

class StudentCreate(BaseModel):
    full_name: str
    class_name: str
    cpf: str
    email: EmailStr
    phone: str
    username: str
    send_email: bool = False

class StudentUpdate(BaseModel):
    full_name: str
    class_name: str
    cpf: str
    email: EmailStr
    phone: str

class StudentResponse(BaseModel):
    id: str
    user_id: str
    full_name: str
    class_name: str
    cpf: str
    email: str
    phone: str
    created_by_user_id: str | None = None
    created_at: datetime

class EnrollmentCreate(BaseModel):
    student_user_id: str
    discipline_id: str

class EnrollmentResponse(BaseModel):
    id: str
    student_user_id: str
    discipline_id: str
    is_active: bool
    created_at: datetime

class AttendanceEventCreate(BaseModel):
    discipline_id: str
    title: str
    lesson_date: str
    lesson_time: str
    allow_remote_requests: bool = False

class AttendanceEventResponse(BaseModel):
    id: str
    discipline_id: str
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
    channel: str = "web"
    stars: int | None = Field(default=None, ge=1, le=5)
    tags: list[str] = Field(default_factory=list)
    comments: str | None = None

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
    discipline_id: str
    status: str
    justification: str | None = None
    updated_at: datetime
