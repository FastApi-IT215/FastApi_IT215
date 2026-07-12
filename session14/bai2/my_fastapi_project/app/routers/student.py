from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services import student as student_service

router = APIRouter(prefix="/students", tags=["students"])

@router.get("", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return student_service.get_all_students(db)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.get_student_by_id(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("", response_model=StudentResponse)
def create_student(student_data: StudentCreate, db: Session = Depends(get_db)):
    return student_service.create_student(db, student_data)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = student_service.update_student(db, student_id, student_data)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = student_service.delete_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
