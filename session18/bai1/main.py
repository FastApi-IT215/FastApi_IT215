from fastapi import FastAPI
from database import engine, Base
from bai1.app.routers.enrollment_router import router as enrollment_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(enrollment_router)