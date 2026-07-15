from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from app.models.workshop_model import StudentModel, WorkshopModel, RegistrationModel
from app.schemas.workshop_schema import (
    StudentCreate, StudentResponse,
    WorkshopCreate, WorkshopResponse,
    RegistrationCreate, RegistrationResponse,
    StudentWithWorkshops, WorkshopWithStudents
)

router = APIRouter()

@router.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    dup_code = db.query(StudentModel).filter(StudentModel.student_code == payload.student_code).first()
    if dup_code:
        raise HTTPException(status_code=400, detail="Student code already exists")
    
    dup_email = db.query(StudentModel).filter(StudentModel.email == payload.email).first()
    if dup_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_student = StudentModel(**payload.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()

@router.post("/workshops", response_model=WorkshopResponse, status_code=status.HTTP_201_CREATED)
def create_workshop(payload: WorkshopCreate, db: Session = Depends(get_db)):
    new_workshop = WorkshopModel(**payload.model_dump())
    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)
    return new_workshop

@router.get("/workshops", response_model=List[WorkshopResponse])
def get_workshops(db: Session = Depends(get_db)):
    return db.query(WorkshopModel).all()

@router.get("/workshops/{id}", response_model=WorkshopResponse)
def get_workshop_by_id(id: int, db: Session = Depends(get_db)):
    workshop = db.query(WorkshopModel).filter(WorkshopModel.id == id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")
    return workshop

@router.post("/registrations", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_workshop(payload: RegistrationCreate, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    workshop = db.query(WorkshopModel).filter(WorkshopModel.id == payload.workshop_id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Student is INACTIVE")

    if workshop.status != "OPEN":
        raise HTTPException(status_code=400, detail="Workshop is closed or not open for registration")

    if workshop.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Workshop has already started")

    dup_reg = db.query(RegistrationModel).filter(
        RegistrationModel.student_id == payload.student_id,
        RegistrationModel.workshop_id == payload.workshop_id,
        RegistrationModel.status == "REGISTERED"
    ).first()
    if dup_reg:
        raise HTTPException(status_code=400, detail="Student has already registered for this workshop")

    current_registrations_count = db.query(RegistrationModel).filter(
        RegistrationModel.workshop_id == payload.workshop_id,
        RegistrationModel.status == "REGISTERED"
    ).count()
    if current_registrations_count >= workshop.maximum_participants:
        raise HTTPException(status_code=400, detail="Workshop limit reached")

    existing_cancelled = db.query(RegistrationModel).filter(
        RegistrationModel.student_id == payload.student_id,
        RegistrationModel.workshop_id == payload.workshop_id,
        RegistrationModel.status == "CANCELLED"
    ).first()

    if existing_cancelled:
        existing_cancelled.status = "REGISTERED"
        existing_cancelled.registered_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_cancelled)
        return existing_cancelled

    new_reg = RegistrationModel(
        student_id=payload.student_id,
        workshop_id=payload.workshop_id
    )
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)
    return new_reg

@router.get("/students/{id}/workshops", response_model=StudentWithWorkshops)
def get_student_workshops(id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    workshops = []
    for reg in student.registrations:
        if reg.status == "REGISTERED":
            workshops.append(reg.workshop)

    return StudentWithWorkshops(
        id=student.id,
        student_code=student.student_code,
        full_name=student.full_name,
        workshops=workshops
    )

@router.get("/workshops/{id}/students", response_model=WorkshopWithStudents)
def get_workshop_students(id: int, db: Session = Depends(get_db)):
    workshop = db.query(WorkshopModel).filter(WorkshopModel.id == id).first()
    if not workshop:
        raise HTTPException(status_code=404, detail="Workshop not found")

    students = []
    for reg in workshop.registrations:
        if reg.status == "REGISTERED":
            students.append(reg.student)

    return WorkshopWithStudents(
        id=workshop.id,
        title=workshop.title,
        students=students
    )

@router.put("/registrations/{id}/cancel", response_model=RegistrationResponse)
def cancel_registration(id: int, db: Session = Depends(get_db)):
    reg = db.query(RegistrationModel).filter(RegistrationModel.id == id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    if reg.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Registration is already cancelled")

    if reg.workshop.start_time <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Cannot cancel registration after workshop started")

    reg.status = "CANCELLED"
    db.commit()
    db.refresh(reg)
    return reg