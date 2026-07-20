"""
Concilium IQ™ — Risk Engine
Calculates cardiovascular risk scores
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PatientRiskData:
    age: int
    sex: str
    has_ascvd: bool = False
    has_diabetes: bool = False
    ldl_c: Optional[float] = None
    apob: Optional[float] = None
    hba1c: Optional[float] = None
    hs_crp: Optional[float] = None


class RiskEngine:
    """Cardiovascular Risk Assessment Engine"""

    def calculate_ascvd_risk(self, data: PatientRiskData) -> float:
        """Calculate 10-year ASCVD risk (simplified placeholder)"""
        base_risk = 5.0
        if data.age > 50:
            base_risk += (data.age - 50) * 0.5
        if data.sex.lower() == "male":
            base_risk *= 1.3
        if data.has_diabetes:
            base_risk *= 2.0
        if data.ldl_c and data.ldl_c > 130:
            base_risk += (data.ldl_c - 130) * 0.1
        return min(base_risk, 100.0)

    def get_risk_category(self, risk_score: float) -> str:
        """Categorize risk level"""
        if risk_score >= 20:
            return "very_high"
        elif risk_score >= 10:
            return "high"
        elif risk_score >= 5:
            return "moderate"
        else:
            return "low"

    def get_ldl_target(self, risk_category: str) -> Optional[float]:
        """Get LDL-C target based on risk category"""
        targets = {
            "very_high": 55.0,
            "high": 70.0,
            "moderate": 100.0,
            "low": 116.0,
        }
        return targets.get(risk_category)
