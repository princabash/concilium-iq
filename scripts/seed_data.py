"""
Concilium IQ™ — Seed Data Script
Creates 3 test patients with realistic clinical data for development/testing.

Run: docker-compose exec backend python scripts/seed_data.py
"""

import asyncio
import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import async_session_maker
from app.models.patient import Patient
from app.models.lab import LabResult


# Test patient fixtures
TEST_PATIENTS = [
    {
        "patient_id": "PAT-001",
        "first_name": "George",
        "last_name": "Anderson",
        "date_of_birth": "1965-03-15",
        "sex": "male",
        "biological_sex": "male",
        "email": "george.anderson@example.com",
        "phone": "+1-555-0101",
        "is_active": True,
        "labs": {
            "test_date": "2026-06-15",
            "ldl_c_mgdl": 145.0,
            "hdl_c_mgdl": 38.0,
            "total_cholesterol_mgdl": 240.0,
            "triglycerides_mgdl": 180.0,
            "apob_mgdl": 130.0,
            "hba1c_percent": 6.8,
            "hs_crp_mg_l": 3.5,
            "creatinine_mgdl": 1.1,
            "alt_u_l": 45.0,
            "ast_u_l": 38.0,
        }
    },
    {
        "patient_id": "PAT-002",
        "first_name": "Maria",
        "last_name": "Garcia",
        "date_of_birth": "1972-08-22",
        "sex": "female",
        "biological_sex": "female",
        "email": "maria.garcia@example.com",
        "phone": "+1-555-0102",
        "is_active": True,
        "labs": {
            "test_date": "2026-06-20",
            "ldl_c_mgdl": 128.0,
            "hdl_c_mgdl": 52.0,
            "total_cholesterol_mgdl": 210.0,
            "triglycerides_mgdl": 150.0,
            "apob_mgdl": 105.0,
            "hba1c_percent": 7.2,
            "hs_crp_mg_l": 2.1,
            "creatinine_mgdl": 0.9,
            "alt_u_l": 30.0,
            "ast_u_l": 28.0,
        }
    },
    {
        "patient_id": "PAT-003",
        "first_name": "James",
        "last_name": "Wilson",
        "date_of_birth": "1988-11-05",
        "sex": "male",
        "biological_sex": "male",
        "email": "james.wilson@example.com",
        "phone": "+1-555-0103",
        "is_active": True,
        "labs": {
            "test_date": "2026-06-25",
            "ldl_c_mgdl": 95.0,
            "hdl_c_mgdl": 65.0,
            "total_cholesterol_mgdl": 175.0,
            "triglycerides_mgdl": 90.0,
            "apob_mgdl": 85.0,
            "hba1c_percent": 5.4,
            "hs_crp_mg_l": 0.8,
            "creatinine_mgdl": 0.95,
            "alt_u_l": 22.0,
            "ast_u_l": 20.0,
        }
    },
]


async def seed_patients():
    """Create test patients with lab results"""
    async with async_session_maker() as session:
        for patient_data in TEST_PATIENTS:
            labs_data = patient_data.pop("labs")

            # Check if patient already exists
            result = await session.execute(
                select(Patient).where(Patient.patient_id == patient_data["patient_id"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"⚠️  Patient {patient_data['patient_id']} already exists, skipping...")
                continue

            # Create patient
            patient = Patient(**patient_data)
            session.add(patient)
            await session.flush()

            # Create lab result
            lab = LabResult(
                patient_id=patient.id,
                **labs_data
            )
            session.add(lab)

            print(f"✅ Created patient {patient.patient_id}: {patient.first_name} {patient.last_name}")

        await session.commit()
        print(f"\n🎉 Seeded {len(TEST_PATIENTS)} test patients successfully!")


if __name__ == "__main__":
    asyncio.run(seed_patients())
