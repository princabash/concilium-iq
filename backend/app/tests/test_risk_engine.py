"""
Concilium IQ™ — Risk Engine Tests
"""

import pytest
from app.core.risk_engine import RiskEngine, PatientRiskData


class TestRiskEngine:
    def setup_method(self):
        self.engine = RiskEngine()

    def test_low_risk_young_female(self):
        data = PatientRiskData(age=30, sex="female", ldl_c=100)
        score = self.engine.calculate_ascvd_risk(data)
        assert score < 5
        assert self.engine.get_risk_category(score) == "low"

    def test_high_risk_diabetic_male(self):
        data = PatientRiskData(age=60, sex="male", has_diabetes=True, ldl_c=150)
        score = self.engine.calculate_ascvd_risk(data)
        assert score >= 10
        assert self.engine.get_risk_category(score) == "high"

    def test_very_high_risk_ascvd(self):
        data = PatientRiskData(age=70, sex="male", has_ascvd=True, ldl_c=120)
        score = self.engine.calculate_ascvd_risk(data)
        assert score >= 20
        assert self.engine.get_risk_category(score) == "very_high"

    def test_ldl_targets(self):
        assert self.engine.get_ldl_target("very_high") == 55.0
        assert self.engine.get_ldl_target("high") == 70.0
        assert self.engine.get_ldl_target("moderate") == 100.0
        assert self.engine.get_ldl_target("low") == 116.0
