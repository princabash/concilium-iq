"""
Concilium IQ™ — Patient Model
"""

from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    sex = Column(String(20), nullable=True)
    biological_sex = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    bmi = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
