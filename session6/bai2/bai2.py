from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Student Management API",
    version="1.0"
)

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]


class StudentCreate(BaseModel):
    code: str
    name: str
    email: str
    age: int



@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):

    for stu in students:
        if stu["code"] == student.code:
            raise HTTPException(
                status_code=400,
                detail="Code already exists"
            )

    if student.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )

    if student.email.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Email cannot be empty"
        )

    if student.age <= 0:
        raise HTTPException(
            status_code=400,
            detail="Age must be greater than 0"
        )

    new_student = {
        "id": max([s["id"] for s in students]) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }

    students.append(new_student)

    return {
        "message": "Create student successfully",
        "data": new_student
    }



@app.get("/students")
def get_students(
    keyword: str = None,
    min_age: int = None,
    max_age: int = None
):

    result = []

    for stu in students:

        if keyword:
            if (
                keyword.lower() not in stu["name"].lower()
                and keyword.lower() not in stu["code"].lower()
                and keyword.lower() not in stu["email"].lower()
            ):
                continue

        if min_age is not None:
            if stu["age"] < min_age:
                continue

        if max_age is not None:
            if stu["age"] > max_age:
                continue

        result.append(stu)

    return {
        "message": "Get students successfully",
        "data": result
    }



@app.get("/students/{student_id}")
def get_student(student_id: int):

    for stu in students:
        if stu["id"] == student_id:
            return {
                "message": "Found student",
                "data": stu
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )



@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student_update: StudentCreate
):

    for stu in students:

        if stu["id"] == student_id:

            for item in students:
                if item["code"] == student_update.code and item["id"] != student_id:
                    raise HTTPException(
                        status_code=400,
                        detail="Code already exists"
                    )

            if student_update.name.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Name cannot be empty"
                )

            if student_update.email.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Email cannot be empty"
                )

            if student_update.age <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Age must be greater than 0"
                )

            stu["code"] = student_update.code
            stu["name"] = student_update.name
            stu["email"] = student_update.email
            stu["age"] = student_update.age

            return {
                "message": "Update student successfully",
                "data": stu
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )



@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    for stu in students:

        if stu["id"] == student_id:

            students.remove(stu)

            return {
                "message": "Delete student successfully",
                "data": stu
            }

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )