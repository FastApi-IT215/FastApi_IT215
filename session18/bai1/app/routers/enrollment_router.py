from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from bai1.app.models.enrollment_model import StudentModel, CourseModel, EnrollmentModel
from bai1.app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse, StudentCoursesResponse, CourseResponse

router = APIRouter()

@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_course(payload: EnrollmentCreate, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(CourseModel).filter(CourseModel.id == payload.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if student.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Student is INACTIVE")

    if course.status != "OPEN":
        raise HTTPException(status_code=400, detail="Course is CLOSED")

    is_enrolled = db.query(EnrollmentModel).filter(
        EnrollmentModel.student_id == payload.student_id,
        EnrollmentModel.course_id == payload.course_id
    ).first()
    if is_enrolled:
        raise HTTPException(status_code=400, detail="Student has already enrolled in this course")

    current_enrollments_count = db.query(EnrollmentModel).filter(
        EnrollmentModel.course_id == payload.course_id
    ).count()
    if current_enrollments_count >= course.max_students:
        raise HTTPException(status_code=400, detail="Course limit reached")

    new_enrollment = EnrollmentModel(
        student_id=payload.student_id,
        course_id=payload.course_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment

@router.get("/students/{student_id}/courses", response_model=StudentCoursesResponse)
def get_student_courses(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    courses_list = []
    for enrollment in student.enrollments:
        courses_list.append(
            CourseResponse(
                id=enrollment.course.id,
                name=enrollment.course.name
            )
        )

    return StudentCoursesResponse(
        student_id=student.id,
        full_name=student.full_name,
        courses=courses_list
    )