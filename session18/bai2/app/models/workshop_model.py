from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_code = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="ACTIVE")

    registrations = relationship("RegistrationModel", back_populates="student")


class WorkshopModel(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    maximum_participants = Column(Integer, nullable=False)
    status = Column(String(50), default="OPEN")
    start_time = Column(DateTime, nullable=False)

    registrations = relationship("RegistrationModel", back_populates="workshop")


class RegistrationModel(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="REGISTERED")

    student = relationship("StudentModel", back_populates="registrations")
    workshop = relationship("WorkshopModel", back_populates="registrations")