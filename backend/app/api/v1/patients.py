"""
Concilium IQ™ — Patients Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import async_session_maker
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.patient_service import PatientService

router = APIRouter()


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.post("/", response_model=PatientResponse)
async def create_patient(patient: PatientCreate, db: AsyncSession = Depends(get_db)):
    """Create a new patient"""
    service = PatientService(db)
    return await service.create(patient)


@router.get("/", response_model=List[PatientResponse])
async def list_patients(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """List all patients"""
    service = PatientService(db)
    return await service.list(skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db)):
    """Get patient by ID"""
    service = PatientService(db)
    patient = await service.get_by_patient_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
