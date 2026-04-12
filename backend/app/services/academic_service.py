from fastapi import HTTPException, status
from app.repositories.class_repository import ClassRepository
from app.repositories.discipline_repository import DisciplineRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.academic import ClassCreate, DisciplineCreate, EnrollmentCreate

class AcademicService:
    def __init__(self) -> None:
        self.discipline_repo = DisciplineRepository()
        self.class_repo = ClassRepository()
        self.enrollment_repo = EnrollmentRepository()
        self.user_repo = UserRepository()

    def create_discipline(self, payload: DisciplineCreate) -> dict:
        code = payload.code.strip().upper()
        if self.discipline_repo.get_by_code(code):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Discipline code already exists")
        return self.discipline_repo.create({"name": payload.name.strip(), "code": code, "description": payload.description.strip() if payload.description else None})

    def list_disciplines(self) -> list[dict]:
        return self.discipline_repo.list_all()

    def create_class(self, payload: ClassCreate) -> dict:
        return self.class_repo.create({"name": payload.name.strip(), "semester": payload.semester.strip(), "shift": payload.shift.strip() if payload.shift else None})

    def list_classes(self) -> list[dict]:
        return self.class_repo.list_all()

    def create_enrollment(self, payload: EnrollmentCreate) -> dict:
        user = self.user_repo.get_by_id(payload.student_user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student user not found")
        if user["role"] != "student":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Target user is not a student")
        if not self.class_repo.get_by_id(payload.class_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
        if not self.discipline_repo.get_by_id(payload.discipline_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Discipline not found")
        if self.enrollment_repo.find_active(payload.student_user_id, payload.class_id, payload.discipline_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Enrollment already exists")
        return self.enrollment_repo.create({"student_user_id": payload.student_user_id, "class_id": payload.class_id, "discipline_id": payload.discipline_id})

    def list_enrollments(self) -> list[dict]:
        return self.enrollment_repo.list_all()
