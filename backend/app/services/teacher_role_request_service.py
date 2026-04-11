from fastapi import HTTPException, status

from app.repositories.teacher_role_request_repository import TeacherRoleRequestRepository
from app.repositories.user_repository import UserRepository


class TeacherRoleRequestService:
    def __init__(
        self,
        request_repo: TeacherRoleRequestRepository | None = None,
        user_repo: UserRepository | None = None,
    ) -> None:
        self.request_repo = request_repo or TeacherRoleRequestRepository()
        self.user_repo = user_repo or UserRepository()

    def create_request(self, user: dict, justification: str) -> dict:
        if user["role"] in {"teacher", "admin"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already has elevated role")
        if self.request_repo.get_pending_for_user(user["id"]):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pending request already exists")
        return self.request_repo.create(user=user, justification=justification)

    def list_pending(self) -> list[dict]:
        return self.request_repo.list_pending()

    def approve(self, request_id: str, admin_user: dict) -> dict:
        request = self.request_repo.get_by_id(request_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request["status"] != "pending":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request already reviewed")

        self.user_repo.update_role(request["user_id"], "teacher")
        self.request_repo.review(request_id=request_id, status="approved", reviewed_by=admin_user["id"])
        request["status"] = "approved"
        request["reviewed_by"] = admin_user["id"]
        return request

    def deny(self, request_id: str, admin_user: dict) -> dict:
        request = self.request_repo.get_by_id(request_id)
        if not request:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        if request["status"] != "pending":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request already reviewed")

        self.request_repo.review(request_id=request_id, status="denied", reviewed_by=admin_user["id"])
        request["status"] = "denied"
        request["reviewed_by"] = admin_user["id"]
        return request
