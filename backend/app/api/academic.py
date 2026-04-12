from fastapi import APIRouter, Depends, status

from app.deps.auth import require_admin
from app.schemas.academic import (
    ClassCreate,
    ClassResponse,
    DisciplineCreate,
    DisciplineResponse,
    EnrollmentCreate,
    EnrollmentResponse,
)
from app.services.academic_service import AcademicService

router = APIRouter(prefix="/academic", tags=["academic"])


@router.post("/disciplines", response_model=DisciplineResponse, status_code=status.HTTP_201_CREATED)
def create_discipline(payload: DisciplineCreate, admin_user: dict = Depends(require_admin)) -> DisciplineResponse:
    result = AcademicService().create_discipline(payload)
    return DisciplineResponse(**result)


@router.get("/disciplines", response_model=list[DisciplineResponse])
def list_disciplines(admin_user: dict = Depends(require_admin)) -> list[DisciplineResponse]:
    results = AcademicService().list_disciplines()
    return [DisciplineResponse(**item) for item in results]


@router.post("/classes", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(payload: ClassCreate, admin_user: dict = Depends(require_admin)) -> ClassResponse:
    result = AcademicService().create_class(payload)
    return ClassResponse(**result)


@router.get("/classes", response_model=list[ClassResponse])
def list_classes(admin_user: dict = Depends(require_admin)) -> list[ClassResponse]:
    results = AcademicService().list_classes()
    return [ClassResponse(**item) for item in results]


@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def create_enrollment(payload: EnrollmentCreate, admin_user: dict = Depends(require_admin)) -> EnrollmentResponse:
    result = AcademicService().create_enrollment(payload)
    return EnrollmentResponse(**result)


@router.get("/enrollments", response_model=list[EnrollmentResponse])
def list_enrollments(admin_user: dict = Depends(require_admin)) -> list[EnrollmentResponse]:
    results = AcademicService().list_enrollments()
    return [EnrollmentResponse(**item) for item in results]
