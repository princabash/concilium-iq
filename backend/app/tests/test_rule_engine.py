"""
Concilium IQ™ — Rule Engine Tests
"""

import pytest
from app.core.risk_engine import RiskEngine, PatientRiskData
from app.core.rule_engine import ClinicalRuleEngine


class TestRuleEngine:
    def setup_method(self):
        self.risk_engine = RiskEngine()
        self.rule_engine = ClinicalRuleEngine(self.risk_engine)

    def test_care_gap_ldl_above_target(self):
        data = PatientRiskData(age=65, sex="male", ldl_c=145)
        result = self.rule_engine.evaluate_patient(data)

        assert "care_gaps" in result
        ldl_gaps = [g for g in result["care_gaps"] if g.type == "ldl_above_target"]
        assert len(ldl_gaps) > 0

    def test_suggested_action_statin(self):
        data = PatientRiskData(age=70, sex="male", has_diabetes=True, ldl_c=130)
        result = self.rule_engine.evaluate_patient(data)

        assert "suggested_actions" in result
        statin_actions = [a for a in result["suggested_actions"] if a.type == "statin_therapy"]
        assert len(statin_actions) > 0

    def test_hba1c_care_gap(self):
        data = PatientRiskData(age=55, sex="female", hba1c=8.5)
        result = self.rule_engine.evaluate_patient(data)

        hba1c_gaps = [g for g in result["care_gaps"] if g.type == "hba1c_above_target"]
        assert len(hba1c_gaps) > 0

    def test_lifestyle_counseling_always_present(self):
        data = PatientRiskData(age=40, sex="female", ldl_c=90)
        result = self.rule_engine.evaluate_patient(data)

        lifestyle = [a for a in result["suggested_actions"] if a.type == "lifestyle_counseling"]
        assert len(lifestyle) > 0
