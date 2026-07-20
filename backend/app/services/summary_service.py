"""
Concilium IQ™ — Summary Service
Generates comprehensive patient clinical intelligence summary
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from datetime import datetime

from app.models.patient import Patient
from app.models.lab import LabResult
from app.schemas.summary import (
    PatientSummary, Demographics, Diagnoses, RiskProfile,
    LatestLabs, BloodPressure, TherapyInfo, LipidHistory,
    CareGap as CareGapSchema, SuggestedAction as SuggestedActionSchema,
    Explanation, LabValue
)
from app.core.risk_engine import RiskEngine, PatientRiskData
from app.core.rule_engine import ClinicalRuleEngine
from app.core.explainability import ExplainabilityEngine
from app.services.patient_service import PatientService


class SummaryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.risk_engine = RiskEngine()
        self.rule_engine = ClinicalRuleEngine(self.risk_engine)
        self.explainability = ExplainabilityEngine()

    async def generate_summary(self, patient_id: str) -> Optional[PatientSummary]:
        """Generate complete clinical intelligence summary for a patient"""

        # Fetch patient
        patient_service = PatientService(self.db)
        patient = await patient_service.get_by_patient_id(patient_id)
        if not patient:
            return None

        # Fetch latest labs
        latest_labs_result = await self.db.execute(
            select(LabResult)
            .where(LabResult.patient_id == patient.id)
            .order_by(desc(LabResult.test_date))
            .limit(1)
        )
        latest_labs = latest_labs_result.scalar_one_or_none()

        # Build PatientRiskData for engines
        risk_data = PatientRiskData(
            age=patient.age if hasattr(patient, "age") else 50,
            sex=patient.biological_sex or patient.sex or "male",
            has_ascvd=False,
            has_diabetes=False,
            ldl_c=float(latest_labs.ldl_c_mgdl) if latest_labs and latest_labs.ldl_c_mgdl else None,
            apob=float(latest_labs.apob_mgdl) if latest_labs and latest_labs.apob_mgdl else None,
            hba1c=float(latest_labs.hba1c_percent) if latest_labs and latest_labs.hba1c_percent else None,
            hs_crp=float(latest_labs.hs_crp_mg_l) if latest_labs and latest_labs.hs_crp_mg_l else None,
        )

        # Run clinical intelligence
        evaluation = self.rule_engine.evaluate_patient(risk_data)

        # Build summary
        return PatientSummary(
            patient_id=patient.patient_id,
            generated_at=datetime.now(),
            demographics=Demographics(
                age=risk_data.age,
                sex=patient.sex or "unknown",
                biological_sex=patient.biological_sex,
                bmi=float(patient.bmi) if patient.bmi else None,
            ),
            diagnoses=Diagnoses(),
            risk=RiskProfile(
                risk_category=evaluation["risk_category"],
                ldl_target_mgdl=evaluation["targets"].get("ldl"),
                apob_target_mgdl=evaluation["targets"].get("apob"),
                non_hdl_target_mgdl=evaluation["targets"].get("non_hdl"),
            ),
            latest_labs=self._build_latest_labs(latest_labs),
            latest_bp=BloodPressure(),
            therapy=TherapyInfo(),
            care_gaps=[
                CareGapSchema(
                    type=g.type,
                    severity=g.severity,
                    description=g.description,
                    guideline_reference=g.guideline_reference,
                )
                for g in evaluation["care_gaps"]
            ],
            suggested_actions=[
                SuggestedActionSchema(
                    type=a.type,
                    priority=a.priority,
                    description=a.description,
                    evidence_reference=a.evidence_reference,
                    rationale=a.rationale,
                )
                for a in evaluation["suggested_actions"]
            ],
            explanation=Explanation(
                rule_trace=self.explainability.generate_rule_trace(risk_data, evaluation),
                confidence_score=95.0,
                model_version="1.0.0",
            ),
        )

    def _build_latest_labs(self, labs: Optional[LabResult]) -> LatestLabs:
        """Build LatestLabs schema from database model"""
        if not labs:
            return LatestLabs()

        return LatestLabs(
            test_date=labs.test_date,
            ldl_c=LabValue(
                value=float(labs.ldl_c_mgdl) if labs.ldl_c_mgdl else None,
                unit="mg/dL",
                status="above_target" if labs.ldl_c_mgdl and labs.ldl_c_mgdl > 100 else "optimal",
            ) if labs.ldl_c_mgdl else None,
            apob=LabValue(
                value=float(labs.apob_mgdl) if labs.apob_mgdl else None,
                unit="mg/dL",
            ) if labs.apob_mgdl else None,
            hba1c=LabValue(
                value=float(labs.hba1c_percent) if labs.hba1c_percent else None,
                unit="%",
            ) if labs.hba1c_percent else None,
        )
