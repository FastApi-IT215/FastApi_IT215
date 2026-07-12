from fastapi import FastAPI
from app.database import Base, engine
from app.routers.product import router as product_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Management API")

app.include_router(product_router)
