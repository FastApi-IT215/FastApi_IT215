from sqlalchemy.orm import Session
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate

def get_all_students(db: Session):
    return db.query(Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student_data: StudentCreate):
    new_student = Student(
        full_name=student_data.full_name,
        email=student_data.email,
        major=student_data.major,
        gpa=student_data.gpa
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def update_student(db: Session, student_id: int, student_data: StudentUpdate):
    student = get_student_by_id(db, student_id)
    if student is None:
        return None
    student.full_name = student_data.full_name
    student.email = student_data.email
    student.major = student_data.major
    student.gpa = student_data.gpa
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if student is None:
        return None
    db.delete(student)
    db.commit()
    return student
