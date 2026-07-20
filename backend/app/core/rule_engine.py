"""
Concilium IQ™ — Clinical Rule Engine
Applies evidence-based clinical guidelines
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from app.core.risk_engine import RiskEngine, PatientRiskData


@dataclass
class CareGap:
    type: str
    severity: str
    description: str
    guideline_reference: Optional[str] = None


@dataclass
class SuggestedAction:
    type: str
    priority: str
    description: str
    evidence_reference: Optional[str] = None
    rationale: Optional[str] = None


class ClinicalRuleEngine:
    """Clinical Guideline Rule Engine"""

    def __init__(self, risk_engine: RiskEngine):
        self.risk_engine = risk_engine

    def evaluate_patient(self, data: PatientRiskData) -> Dict[str, Any]:
        """Evaluate patient against clinical rules"""

        # Calculate risk
        risk_score = self.risk_engine.calculate_ascvd_risk(data)
        risk_category = self.risk_engine.get_risk_category(risk_score)

        # Determine targets
        targets = {
            "ldl": self.risk_engine.get_ldl_target(risk_category),
            "apob": 80.0 if risk_category in ["very_high", "high"] else 100.0,
            "non_hdl": 85.0 if risk_category in ["very_high", "high"] else 130.0,
        }

        # Identify care gaps
        care_gaps = self._identify_care_gaps(data, risk_category, targets)

        # Generate suggested actions
        suggested_actions = self._generate_actions(data, risk_category, care_gaps)

        return {
            "risk_score": risk_score,
            "risk_category": risk_category,
            "targets": targets,
            "care_gaps": care_gaps,
            "suggested_actions": suggested_actions,
        }

    def _identify_care_gaps(self, data: PatientRiskData, risk_category: str, targets: Dict) -> List[CareGap]:
        """Identify care gaps based on guidelines"""
        gaps = []

        # LDL-C gap
        if data.ldl_c and targets.get("ldl") and data.ldl_c > targets["ldl"]:
            gaps.append(CareGap(
                type="ldl_above_target",
                severity="high" if risk_category in ["very_high", "high"] else "moderate",
                description=f"LDL-C is {data.ldl_c} mg/dL, target is <{targets['ldl']} mg/dL",
                guideline_reference="ESC/EAS 2019 Dyslipidemia Guidelines",
            ))

        # HbA1c gap
        if data.hba1c and data.hba1c > 7.0:
            gaps.append(CareGap(
                type="hba1c_above_target",
                severity="moderate",
                description=f"HbA1c is {data.hba1c}%, target is <7.0%",
                guideline_reference="ADA 2024 Standards of Care",
            ))

        # hs-CRP gap
        if data.hs_crp and data.hs_crp > 3.0:
            gaps.append(CareGap(
                type="inflammation_elevated",
                severity="moderate",
                description=f"hs-CRP is {data.hs_crp} mg/L, indicating elevated inflammation",
                guideline_reference="AHA/CDC Inflammation Statement",
            ))

        return gaps

    def _generate_actions(self, data: PatientRiskData, risk_category: str, gaps: List[CareGap]) -> List[SuggestedAction]:
        """Generate suggested clinical actions"""
        actions = []

        if risk_category in ["very_high", "high"]:
            actions.append(SuggestedAction(
                type="statin_therapy",
                priority="high",
                description="Initiate high-intensity statin therapy",
                evidence_reference="ACC/AHA 2018 Cholesterol Guidelines",
                rationale=f"Patient is {risk_category} risk category",
            ))

        for gap in gaps:
            if gap.type == "ldl_above_target":
                actions.append(SuggestedAction(
                    type="lipid_optimization",
                    priority="high",
                    description="Consider adding ezetimibe or PCSK9 inhibitor",
                    evidence_reference="ESC/EAS 2019",
                    rationale="LDL-C above target despite statin therapy",
                ))
            elif gap.type == "hba1c_above_target":
                actions.append(SuggestedAction(
                    type="diabetes_optimization",
                    priority="moderate",
                    description="Optimize diabetes management",
                    evidence_reference="ADA 2024",
                    rationale="HbA1c above glycemic target",
                ))

        actions.append(SuggestedAction(
            type="lifestyle_counseling",
            priority="moderate",
            description="Provide lifestyle modification counseling (diet, exercise, smoking cessation)",
            evidence_reference="AHA Lifestyle Guidelines",
            rationale="Lifestyle modifications are foundational for all risk categories",
        ))

        return actions
