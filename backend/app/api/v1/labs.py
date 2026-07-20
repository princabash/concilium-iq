"""
Concilium IQ™ — Lab Results Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker

router = APIRouter()


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.post("/")
async def create_lab_result(db: AsyncSession = Depends(get_db)):
    """Submit new lab results (placeholder)"""
    return {"message": "Lab result created"}


@router.get("/patient/{patient_id}")
async def get_patient_labs(patient_id: str, db: AsyncSession = Depends(get_db)):
    """Get lab history for a patient (placeholder)"""
    return {"patient_id": patient_id, "labs": []}
