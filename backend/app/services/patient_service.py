"""
Concilium IQ™ — Patient Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientResponse


class PatientService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, patient_data: PatientCreate) -> Patient:
        """Create a new patient"""
        patient = Patient(**patient_data.model_dump())
        self.db.add(patient)
        await self.db.flush()
        await self.db.refresh(patient)
        return patient

    async def get_by_patient_id(self, patient_id: str) -> Optional[Patient]:
        """Get patient by internal patient_id"""
        result = await self.db.execute(
            select(Patient).where(Patient.patient_id == patient_id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        """List patients with pagination"""
        result = await self.db.execute(
            select(Patient).where(Patient.is_active == True)
            .offset(skip).limit(limit)
        )
        return result.scalars().all()
