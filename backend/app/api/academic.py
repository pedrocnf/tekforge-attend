from fastapi import APIRouter, Depends, status
from app.deps.auth import require_admin
from app.schemas.academic import ClassCreate, ClassResponse, DisciplineCreate, DisciplineResponse, EnrollmentCreate, EnrollmentResponse
from app.services.academic_service import AcademicService
router = APIRouter(prefix="/academic", tags=["academic"])
@router.post("/disciplines", response_model=DisciplineResponse, status_code=status.HTTP_201_CREATED)
def create_discipline(payload: DisciplineCreate, admin_user: dict = Depends(require_admin)) -> DisciplineResponse:
    return DisciplineResponse(**AcademicService().create_discipline(payload))
@router.get("/disciplines", response_model=list[DisciplineResponse])
def list_disciplines(admin_user: dict = Depends(require_admin)) -> list[DisciplineResponse]:
    return [DisciplineResponse(**item) for item in AcademicService().list_disciplines()]
@router.post("/classes", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(payload: ClassCreate, admin_user: dict = Depends(require_admin)) -> ClassResponse:
    return ClassResponse(**AcademicService().create_class(payload))
@router.get("/classes", response_model=list[ClassResponse])
def list_classes(admin_user: dict = Depends(require_admin)) -> list[ClassResponse]:
    return [ClassResponse(**item) for item in AcademicService().list_classes()]
@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, admin_user: dict = Depends(require_admin)) -> EnrollmentResponse:
    return EnrollmentResponse(**AcademicService().create_enrollment(payload))
@router.get("/enrollments", response_model=list[EnrollmentResponse])
def list_enrollments(admin_user: dict = Depends(require_admin)) -> list[EnrollmentResponse]:
    return [EnrollmentResponse(**item) for item in AcademicService().list_enrollments()]
