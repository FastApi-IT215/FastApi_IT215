from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class StudentCreate(BaseModel):
    student_code: str
    full_name: str
    email: EmailStr
    status: Optional[str] = "ACTIVE"

class StudentResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: str
    status: str

    class Config:
        from_attributes = True

class WorkshopCreate(BaseModel):
    title: str
    description: Optional[str] = None
    maximum_participants: int
    status: Optional[str] = "OPEN"
    start_time: datetime

class WorkshopResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    maximum_participants: int
    status: str
    start_time: datetime

    class Config:
        from_attributes = True

class RegistrationCreate(BaseModel):
    student_id: int
    workshop_id: int

class RegistrationResponse(BaseModel):
    id: int
    student_id: int
    workshop_id: int
    registered_at: datetime
    status: str

    class Config:
        from_attributes = True

class StudentWithWorkshops(BaseModel):
    id: int
    student_code: str
    full_name: str
    workshops: List[WorkshopResponse]

    class Config:
        from_attributes = True

class WorkshopWithStudents(BaseModel):
    id: int
    title: str
    students: List[StudentResponse]

    class Config:
        from_attributes = True