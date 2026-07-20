"""
Concilium IQ™ — Summary Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LabValue(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[str] = None


class Demographics(BaseModel):
    age: Optional[int] = None
    sex: Optional[str] = None
    biological_sex: Optional[str] = None
    bmi: Optional[float] = None


class Diagnoses(BaseModel):
    pass


class RiskProfile(BaseModel):
    risk_category: Optional[str] = None
    ldl_target_mgdl: Optional[float] = None
    apob_target_mgdl: Optional[float] = None
    non_hdl_target_mgdl: Optional[float] = None


class LatestLabs(BaseModel):
    test_date: Optional[datetime] = None
    ldl_c: Optional[LabValue] = None
    apob: Optional[LabValue] = None
    hba1c: Optional[LabValue] = None


class BloodPressure(BaseModel):
    pass


class TherapyInfo(BaseModel):
    pass


class LipidHistory(BaseModel):
    pass


class CareGap(BaseModel):
    type: str
    severity: str
    description: str
    guideline_reference: Optional[str] = None


class SuggestedAction(BaseModel):
    type: str
    priority: str
    description: str
    evidence_reference: Optional[str] = None
    rationale: Optional[str] = None


class Explanation(BaseModel):
    rule_trace: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    model_version: Optional[str] = None


class PatientSummary(BaseModel):
    patient_id: str
    generated_at: datetime
    demographics: Demographics
    diagnoses: Diagnoses
    risk: RiskProfile
    latest_labs: LatestLabs
    latest_bp: BloodPressure
    therapy: TherapyInfo
    care_gaps: List[CareGap]
    suggested_actions: List[SuggestedAction]
    explanation: Explanation
