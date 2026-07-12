from fastapi import FastAPI
from app.database import Base, engine
from app.routers.student import router as student_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management API")

app.include_router(student_router)
