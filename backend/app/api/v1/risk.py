"""
Concilium IQ™ — Risk Assessment Router
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_maker

router = APIRouter()


async def get_db():
    async with async_session_maker() as session:
        yield session


@router.get("/patient/{patient_id}")
async def assess_risk(patient_id: str, db: AsyncSession = Depends(get_db)):
    """Assess cardiovascular risk for a patient (placeholder)"""
    return {"patient_id": patient_id, "risk_score": None, "risk_category": None}
