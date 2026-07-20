"""
Concilium IQ™ — Lab Result Model
"""

from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    test_date = Column(Date, nullable=False)

    # Lipid panel
    ldl_c_mgdl = Column(Float, nullable=True)
    hdl_c_mgdl = Column(Float, nullable=True)
    total_cholesterol_mgdl = Column(Float, nullable=True)
    triglycerides_mgdl = Column(Float, nullable=True)
    apob_mgdl = Column(Float, nullable=True)

    # Metabolic
    hba1c_percent = Column(Float, nullable=True)
    hs_crp_mg_l = Column(Float, nullable=True)

    # Liver & Kidney
    creatinine_mgdl = Column(Float, nullable=True)
    alt_u_l = Column(Float, nullable=True)
    ast_u_l = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
