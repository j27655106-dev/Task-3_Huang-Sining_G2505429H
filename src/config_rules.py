"""
Jurisdiction configuration layer.

This file is the core 'jurisdiction-aware' component of the prototype.
It translates legal/regulatory sources into operational compliance checks.
The thresholds are illustrative and are not legal advice.
"""

JURISDICTION_RULES = {
    "US": {
        "name": "United States",
        "regime": "ECOA / Regulation B-style fair lending review",
        "rule_version": "US-2026-05-demo",
        "last_reviewed": "2026-05-22",
        "regulatory_philosophy": "Outcome fairness, adverse action explanation, and post-hoc review",
        "sources": [
            {
                "rule_id": "US-CFPB-ADVERSE-ACTION",
                "source_name": "CFPB guidance on AI-driven credit decisions and adverse action notices",
                "url": "https://www.consumerfinance.gov/about-us/newsroom/cfpb-issues-guidance-on-credit-denials-by-lenders-using-artificial-intelligence/",
                "operational_test": "Rejected applicants must receive specific and meaningful adverse action reasons."
            },
            {
                "rule_id": "US-REG-B",
                "source_name": "ECOA / Regulation B fair lending logic",
                "url": "https://www.consumerfinance.gov/",
                "operational_test": "Check whether approval outcomes differ materially across protected or proxy groups."
            }
        ],
        "approval_disparity_threshold": 0.80,
        "requires_adverse_action_reasons": True,
        "requires_bias_testing": True,
        "requires_model_card": True,
        "requires_human_oversight": False,
        "requires_drift_monitoring": True,
        "high_risk_ai_classification": False,
    },
    "UK": {
        "name": "United Kingdom",
        "regime": "FCA Consumer Duty and responsible lending outcome monitoring",
        "rule_version": "UK-2026-05-demo",
        "last_reviewed": "2026-05-22",
        "regulatory_philosophy": "Consumer outcomes, responsible lending, explainability, and board-level accountability",
        "sources": [
            {
                "rule_id": "UK-FCA-CONSUMER-DUTY",
                "source_name": "FCA Consumer Duty outcome monitoring",
                "url": "https://www.fca.org.uk/news/blogs/year-2-consumer-duty-board-reports-progress-and-what-comes-next",
                "operational_test": "Monitor whether credit decisions create poor outcomes for customer groups."
            },
            {
                "rule_id": "UK-FCA-IMPLEMENTATION-PLANS",
                "source_name": "FCA Consumer Duty implementation planning",
                "url": "https://www.fca.org.uk/publications/multi-firm-reviews/consumer-duty-implementation-plans",
                "operational_test": "Require evidence that governance, monitoring, and remediation are embedded in the product lifecycle."
            }
        ],
        "approval_disparity_threshold": 0.90,
        "requires_adverse_action_reasons": True,
        "requires_bias_testing": True,
        "requires_model_card": True,
        "requires_human_oversight": True,
        "requires_drift_monitoring": True,
        "requires_consumer_duty_outcome_monitoring": True,
        "high_risk_ai_classification": False,
    }
}

MODEL_RISK_REFERENCE = {
    "source_name": "OCC Bulletin 2026-13: Model Risk Management Revised Guidance",
    "url": "https://www.occ.treas.gov/news-issuances/bulletins/2026/bulletin-2026-13.html",
    "operational_relevance": "Use risk-based model monitoring and lifecycle controls. This prototype implements model card, drift simulation, and monitoring logic."
}
