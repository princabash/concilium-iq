"""
Concilium IQ™ — Patient Schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from uuid import UUID


class PatientBase(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    sex: Optional[str] = None
    biological_sex: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    bmi: Optional[float] = None


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True
