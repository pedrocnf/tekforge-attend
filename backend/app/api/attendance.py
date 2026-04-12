from fastapi import APIRouter, Depends, status
from app.deps.auth import get_current_user, require_teacher_or_admin
from app.schemas.attendance import AttendanceDecision, AttendanceEventCreate, AttendanceEventResponse, AttendanceFinalRecordResponse, AttendanceRequestCreate, AttendanceRequestResponse
from app.services.attendance_service import AttendanceService
router = APIRouter(prefix="/attendance", tags=["attendance"])
@router.post("/events", response_model=AttendanceEventResponse, status_code=status.HTTP_201_CREATED)
def create_event(payload: AttendanceEventCreate, actor: dict = Depends(require_teacher_or_admin)) -> AttendanceEventResponse:
    return AttendanceEventResponse(**AttendanceService().create_event(payload, actor))
@router.get("/events", response_model=list[AttendanceEventResponse])
def list_events(actor: dict = Depends(require_teacher_or_admin)) -> list[AttendanceEventResponse]:
    return [AttendanceEventResponse(**item) for item in AttendanceService().list_events()]
@router.post("/requests", response_model=AttendanceRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(payload: AttendanceRequestCreate, current_user: dict = Depends(get_current_user)) -> AttendanceRequestResponse:
    return AttendanceRequestResponse(**AttendanceService().create_request(payload))
@router.get("/events/{event_id}/requests", response_model=list[AttendanceRequestResponse])
def list_requests(event_id: str, actor: dict = Depends(require_teacher_or_admin)) -> list[AttendanceRequestResponse]:
    return [AttendanceRequestResponse(**item) for item in AttendanceService().list_requests(event_id)]
@router.post("/requests/{request_id}/review")
def review_request(request_id: str, payload: AttendanceDecision, actor: dict = Depends(require_teacher_or_admin)) -> dict:
    return AttendanceService().review_request(request_id, payload.status, actor)
@router.post("/events/{event_id}/close", response_model=AttendanceEventResponse)
def close_event(event_id: str, actor: dict = Depends(require_teacher_or_admin)) -> AttendanceEventResponse:
    return AttendanceEventResponse(**AttendanceService().close_event(event_id))
@router.get("/events/{event_id}/final-records", response_model=list[AttendanceFinalRecordResponse])
def list_final_records(event_id: str, actor: dict = Depends(require_teacher_or_admin)) -> list[AttendanceFinalRecordResponse]:
    return [AttendanceFinalRecordResponse(**item) for item in AttendanceService().list_final_records(event_id)]
