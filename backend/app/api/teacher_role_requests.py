from fastapi import APIRouter, Depends, status

from app.deps.auth import get_current_user, require_admin
from app.schemas.teacher_role_request import (
    TeacherRoleRequestCreate,
    TeacherRoleRequestResponse,
)
from app.services.teacher_role_request_service import TeacherRoleRequestService

router = APIRouter(prefix="/teacher-role-requests", tags=["teacher-role-requests"])


@router.post("", response_model=TeacherRoleRequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(
    payload: TeacherRoleRequestCreate,
    current_user: dict = Depends(get_current_user),
) -> TeacherRoleRequestResponse:
    result = TeacherRoleRequestService().create_request(user=current_user, justification=payload.justification)
    return TeacherRoleRequestResponse(**result)


@router.get("/pending", response_model=list[TeacherRoleRequestResponse])
def list_pending(admin_user: dict = Depends(require_admin)) -> list[TeacherRoleRequestResponse]:
    results = TeacherRoleRequestService().list_pending()
    return [TeacherRoleRequestResponse(**item) for item in results]


@router.post("/{request_id}/approve", response_model=TeacherRoleRequestResponse)
def approve_request(request_id: str, admin_user: dict = Depends(require_admin)) -> TeacherRoleRequestResponse:
    result = TeacherRoleRequestService().approve(request_id=request_id, admin_user=admin_user)
    return TeacherRoleRequestResponse(**result)


@router.post("/{request_id}/deny", response_model=TeacherRoleRequestResponse)
def deny_request(request_id: str, admin_user: dict = Depends(require_admin)) -> TeacherRoleRequestResponse:
    result = TeacherRoleRequestService().deny(request_id=request_id, admin_user=admin_user)
    return TeacherRoleRequestResponse(**result)
