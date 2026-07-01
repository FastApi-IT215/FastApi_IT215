from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Course Management API",
    version="1.0"
)


courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]


class CourseCreate(BaseModel):
    code: str
    name: str
    duration: int
    fee: int


@app.post("/courses")
def create_course(course: CourseCreate):

    for item in courses:
        if item["code"] == course.code:
            raise HTTPException(
                status_code=400,
                detail="Code already exists"
            )

    if course.name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty"
        )
    
    if course.duration <= 0:
        raise HTTPException(
            status_code=400,
            detail="Duration must be greater than 0"
        )

    if course.fee < 0:
        raise HTTPException(
            status_code=400,
            detail="Fee must be greater than or equal to 0"
        )


    new_course = {
        "id": len(courses) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }


    courses.append(new_course)


    return {
        "message": "Create course successfully",
        "data": new_course
    }



@app.get("/courses")
def get_courses(
    keyword: str = None,
    min_fee: int = None,
    max_fee: int = None
):

    result = []


    for course in courses:

        if keyword:

            if (
                keyword.lower() not in course["name"].lower()
                and
                keyword.lower() not in course["code"].lower()
            ):
                continue

        if min_fee is not None:

            if course["fee"] < min_fee:
                continue

        if max_fee is not None:

            if course["fee"] > max_fee:
                continue



        result.append(course)



    return {
        "message": "Get courses successfully",
        "data": result
    }


@app.get("/courses/{course_id}")
def get_course(course_id: int):

    for course in courses:

        if course["id"] == course_id:

            return {
                "message": "Found course",
                "data": course
            }


    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )


@app.put("/courses/{course_id}")
def update_course(
    course_id: int,
    course_update: CourseCreate
):


    for course in courses:

        if course["id"] == course_id:
            for item in courses:

                if item["code"] == course_update.code and item["id"] != course_id:

                    raise HTTPException(
                        status_code=400,
                        detail="Code already exists"
                    )



            if course_update.name.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Name cannot be empty"
                )



            if course_update.duration <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Duration must be greater than 0"
                )



            if course_update.fee < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Fee must be greater than or equal to 0"
                )


            course["code"] = course_update.code
            course["name"] = course_update.name
            course["duration"] = course_update.duration
            course["fee"] = course_update.fee


            return {
                "message": "Update successfully",
                "data": course
            }



    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )



@app.delete("/courses/{course_id}")
def delete_course(course_id: int):


    for course in courses:


        if course["id"] == course_id:


            courses.remove(course)


            return {
                "message": "Delete successfully",
                "data": course
            }



    raise HTTPException(
        status_code=404,
        detail="Course not found"
    )