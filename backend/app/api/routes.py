from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.core.config import settings
from app.core.security import hash_password
from app.deps.auth import get_current_user, require_admin, require_teacher_or_admin
from app.repositories.user_repository import UserRepository
from app.schemas.models import *
from app.services.services import AuthService, InstitutionService, DisciplineService, StudentService, EnrollmentService, AttendanceService

router = APIRouter()

@router.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version, "environment": settings.app_env}

@router.post("/auth/signup", response_model=UserResponse, tags=["auth"], status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest):
    return UserResponse(**AuthService().signup_student(payload))

@router.post("/auth/login", response_model=TokenResponse, tags=["auth"])
def login(payload: LoginRequest):
    return TokenResponse(access_token=AuthService().login(payload))

@router.get("/auth/me", response_model=UserResponse, tags=["auth"])
def me(current_user: dict = Depends(get_current_user)):
    return UserResponse(**current_user)

@router.post("/auth/first-access", tags=["auth"])
def first_access(payload: FirstAccessRequest):
    return AuthService().first_access(payload)

@router.post("/auth/forgot-password", tags=["auth"])
def forgot_password(payload: ForgotPasswordRequest):
    return AuthService().forgot_password(payload)

@router.post("/auth/reset-password", tags=["auth"])
def reset_password(payload: ResetPasswordRequest):
    return AuthService().reset_password(payload)

@router.post("/auth/verify-email", tags=["auth"])
def verify_email(token: str):
    return AuthService().verify_email(token)

@router.post("/admin/bootstrap", tags=["admin"])
def bootstrap_admin(password: str):
    if not settings.enable_admin_bootstrap:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin bootstrap disabled")
    if password != settings.admin_bootstrap_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid bootstrap password")
    repo = UserRepository(); existing = repo.get_by_username(settings.admin_bootstrap_username)
    if existing: return {"status": "already_exists", "username": existing["username"], "role": existing["role"]}
    user = repo.create({"username": settings.admin_bootstrap_username, "password_hash": hash_password(settings.admin_bootstrap_password), "full_name": "Attend Admin", "email": settings.admin_bootstrap_email, "role": "admin", "is_email_verified": True})
    return {"status": "created", "user_id": user["id"], "username": user["username"], "role": user["role"]}

@router.post("/institutions", response_model=InstitutionResponse, tags=["institutions"], status_code=status.HTTP_201_CREATED)
def create_institution(payload: InstitutionCreate, actor: dict = Depends(require_teacher_or_admin)):
    return InstitutionResponse(**InstitutionService().create(payload))

@router.get("/institutions", response_model=list[InstitutionResponse], tags=["institutions"])
def list_institutions(actor: dict = Depends(require_teacher_or_admin)):
    return [InstitutionResponse(**x) for x in InstitutionService().list_all()]

@router.put("/institutions/{institution_id}", response_model=InstitutionResponse, tags=["institutions"])
def update_institution(institution_id: str, payload: InstitutionCreate, actor: dict = Depends(require_teacher_or_admin)):
    return InstitutionResponse(**InstitutionService().update(institution_id, payload))

@router.post("/disciplines", response_model=DisciplineResponse, tags=["disciplines"], status_code=status.HTTP_201_CREATED)
def create_discipline(payload: DisciplineCreate, actor: dict = Depends(require_teacher_or_admin)):
    return DisciplineResponse(**DisciplineService().create(payload))

@router.get("/disciplines", response_model=list[DisciplineResponse], tags=["disciplines"])
def list_disciplines(actor: dict = Depends(require_teacher_or_admin)):
    return [DisciplineResponse(**x) for x in DisciplineService().list_all()]

@router.post("/students", response_model=StudentResponse, tags=["students"], status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, actor: dict = Depends(require_teacher_or_admin)):
    return StudentResponse(**StudentService().create(payload, actor))

@router.get("/students", response_model=list[StudentResponse], tags=["students"])
def list_students(actor: dict = Depends(require_teacher_or_admin)):
    return [StudentResponse(**x) for x in StudentService().list_all()]

@router.put("/students/{student_id}", response_model=StudentResponse, tags=["students"])
def update_student(student_id: str, payload: StudentUpdate, actor: dict = Depends(require_teacher_or_admin)):
    return StudentResponse(**StudentService().update(student_id, payload))

@router.post("/students/import", tags=["students"])
async def import_students(file: UploadFile = File(...), actor: dict = Depends(require_teacher_or_admin)):
    content = await file.read(); return StudentService().import_excel(content, actor)

@router.post("/enrollments", response_model=EnrollmentResponse, tags=["enrollments"], status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, actor: dict = Depends(require_teacher_or_admin)):
    return EnrollmentResponse(**EnrollmentService().create(payload))

@router.get("/enrollments", response_model=list[EnrollmentResponse], tags=["enrollments"])
def list_enrollments(actor: dict = Depends(require_teacher_or_admin)):
    return [EnrollmentResponse(**x) for x in EnrollmentService().list_all()]

@router.post("/attendance/events", response_model=AttendanceEventResponse, tags=["attendance"], status_code=status.HTTP_201_CREATED)
def create_event(payload: AttendanceEventCreate, actor: dict = Depends(require_teacher_or_admin)):
    return AttendanceEventResponse(**AttendanceService().create_event(payload, actor))

@router.get("/attendance/events", response_model=list[AttendanceEventResponse], tags=["attendance"])
def list_events(actor: dict = Depends(require_teacher_or_admin)):
    return [AttendanceEventResponse(**x) for x in AttendanceService().list_events()]

@router.post("/attendance/requests", response_model=AttendanceRequestResponse, tags=["attendance"], status_code=status.HTTP_201_CREATED)
def create_request(payload: AttendanceRequestCreate, actor: dict = Depends(get_current_user)):
    return AttendanceRequestResponse(**AttendanceService().create_request(payload, actor))

@router.get("/attendance/events/{event_id}/requests", response_model=list[AttendanceRequestResponse], tags=["attendance"])
def list_requests(event_id: str, actor: dict = Depends(require_teacher_or_admin)):
    return [AttendanceRequestResponse(**x) for x in AttendanceService().list_requests(event_id)]

@router.post("/attendance/requests/{request_id}/review", tags=["attendance"])
def review_request(request_id: str, payload: AttendanceDecision, actor: dict = Depends(require_teacher_or_admin)):
    return AttendanceService().review_request(request_id, payload.status, actor)

@router.post("/attendance/events/{event_id}/close", response_model=AttendanceEventResponse, tags=["attendance"])
def close_event(event_id: str, actor: dict = Depends(require_teacher_or_admin)):
    return AttendanceEventResponse(**AttendanceService().close_event(event_id))

@router.get("/attendance/events/{event_id}/final-records", response_model=list[AttendanceFinalRecordResponse], tags=["attendance"])
def list_final_records(event_id: str, actor: dict = Depends(require_teacher_or_admin)):
    return [AttendanceFinalRecordResponse(**x) for x in AttendanceService().list_final_records(event_id)]
