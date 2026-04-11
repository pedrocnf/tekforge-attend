from datetime import datetime
from pydantic import BaseModel, Field


class TeacherRoleRequestCreate(BaseModel):
    justification: str = Field(min_length=5, max_length=1000)


class TeacherRoleRequestResponse(BaseModel):
    id: str
    user_id: str
    username: str
    full_name: str
    email: str
    status: str
    justification: str
    requested_at: datetime
    reviewed_at: datetime | None = None
    reviewed_by: str | None = None
