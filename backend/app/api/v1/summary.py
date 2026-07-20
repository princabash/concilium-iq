"""
Concilium IQ™ — Summary Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker
from app.schemas.summary import PatientSummary
from app.services.summary_service import SummaryService

router = APIRouter()


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/{patient_id}", response_model=PatientSummary)
async def get_patient_summary(patient_id: str, db: AsyncSession = Depends(get_db)):
    """Generate clinical intelligence summary for a patient"""
    service = SummaryService(db)
    summary = await service.generate_summary(patient_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Patient not found")
    return summary
