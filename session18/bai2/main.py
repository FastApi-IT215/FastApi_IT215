from fastapi import FastAPI
from database import engine, Base
from app.routers.workshop_router import router as workshop_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(workshop_router)