from datetime import datetime
from pydantic import BaseModel, Field


class DisciplineCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    code: str = Field(min_length=2, max_length=30)
    description: str | None = Field(default=None, max_length=500)


class DisciplineResponse(BaseModel):
    id: str
    name: str
    code: str
    description: str | None = None
    is_active: bool
    created_at: datetime


class ClassCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    semester: str = Field(min_length=2, max_length=30)
    shift: str | None = Field(default=None, max_length=30)


class ClassResponse(BaseModel):
    id: str
    name: str
    semester: str
    shift: str | None = None
    is_active: bool
    created_at: datetime


class EnrollmentCreate(BaseModel):
    student_user_id: str = Field(min_length=4, max_length=100)
    class_id: str = Field(min_length=4, max_length=100)
    discipline_id: str = Field(min_length=4, max_length=100)


class EnrollmentResponse(BaseModel):
    id: str
    student_user_id: str
    class_id: str
    discipline_id: str
    is_active: bool
    created_at: datetime
