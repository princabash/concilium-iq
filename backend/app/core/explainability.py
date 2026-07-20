"""
Concilium IQ™ — Explainability Engine
Generates human-readable explanations for clinical decisions
"""

from typing import List, Dict, Any

from app.core.risk_engine import PatientRiskData


class ExplainabilityEngine:
    """Explainability and Transparency Engine"""

    def generate_rule_trace(self, data: PatientRiskData, evaluation: Dict[str, Any]) -> List[str]:
        """Generate a trace of rules that led to the recommendation"""
        trace = []

        # Risk calculation trace
        trace.append(f"1. Patient age: {data.age} years, sex: {data.sex}")

        if data.has_ascvd:
            trace.append("2. Patient has established ASCVD → Very High Risk category")
        elif data.has_diabetes:
            trace.append("2. Patient has diabetes → High Risk category")
        else:
            trace.append(f"2. Calculated 10-year ASCVD risk: {evaluation['risk_score']:.1f}%")
            trace.append(f"3. Risk category determined as: {evaluation['risk_category'].upper()}")

        # Target determination
        trace.append(f"4. Based on {evaluation['risk_category']} risk, LDL-C target set to <{evaluation['targets'].get('ldl')} mg/dL")

        # Care gaps
        if evaluation['care_gaps']:
            trace.append("5. Identified care gaps:")
            for gap in evaluation['care_gaps']:
                trace.append(f"   • {gap.description} [{gap.guideline_reference}]")

        # Actions
        if evaluation['suggested_actions']:
            trace.append("6. Recommended actions:")
            for action in evaluation['suggested_actions']:
                trace.append(f"   • {action.description} (Priority: {action.priority})")

        return trace

    def generate_patient_friendly_explanation(self, evaluation: Dict[str, Any]) -> str:
        """Generate a patient-friendly explanation"""
        category = evaluation['risk_category']
        explanations = {
            "very_high": "Your cardiovascular risk is very high. This means you have a significant chance of heart attack or stroke in the next 10 years. Immediate action is needed.",
            "high": "Your cardiovascular risk is high. We need to take steps to reduce your risk of heart disease and stroke.",
            "moderate": "Your cardiovascular risk is moderate. Lifestyle changes and possibly medication can help reduce your risk.",
            "low": "Your cardiovascular risk is low. Keep up the good work with healthy habits!",
        }
        return explanations.get(category, "Risk assessment completed.")
