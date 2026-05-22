from __future__ import annotations

from typing import Any, Dict
import pandas as pd

from .config_rules import JURISDICTION_RULES
from .model_pipeline import SENSITIVE_ATTRIBUTES
from .explainability import explain_rejections


def approval_rate_by_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    grouped = df.groupby(group_col)["approved"].agg(["mean", "count"]).reset_index()
    grouped = grouped.rename(columns={"mean": "approval_rate", "count": "n"})
    grouped["approval_rate"] = grouped["approval_rate"].round(3)
    return grouped.sort_values("approval_rate")


def disparity_ratio(df: pd.DataFrame, group_col: str) -> float:
    rates = df.groupby(group_col)["approved"].mean()
    if len(rates) <= 1:
        return 1.0
    max_rate = rates.max()
    min_rate = rates.min()
    return 0.0 if max_rate == 0 else float(min_rate / max_rate)


def run_compliance_check(
    df: pd.DataFrame,
    jurisdiction: str,
    model_card_available: bool = True,
    human_oversight_available: bool = True,
    bias_testing_completed: bool = True,
    drift_monitoring_available: bool = True,
) -> Dict[str, Any]:
    if jurisdiction not in JURISDICTION_RULES:
        raise ValueError(f"Unsupported jurisdiction: {jurisdiction}")

    rules = JURISDICTION_RULES[jurisdiction]
    findings = []
    group_results = {}

    for attr in SENSITIVE_ATTRIBUTES:
        ratio = disparity_ratio(df, attr)
        rates = approval_rate_by_group(df, attr)
        group_results[attr] = {
            "disparity_ratio": round(ratio, 3),
            "approval_rates": rates.to_dict(orient="records")
        }
        if ratio < rules["approval_disparity_threshold"]:
            findings.append({
                "severity": "High" if ratio < 0.70 else "Medium",
                "rule_id": "DISPARITY-MONITORING",
                "finding": f"Approval disparity detected for {attr}",
                "details": f"Disparity ratio {ratio:.3f} is below {jurisdiction} threshold {rules['approval_disparity_threshold']:.2f}."
            })

    if rules["requires_adverse_action_reasons"]:
        rejections = explain_rejections(df, sample_size=20)
        if df["approved"].eq(0).sum() > 0 and rejections.empty:
            findings.append({
                "severity": "High",
                "rule_id": "ADVERSE-ACTION",
                "finding": "Missing adverse action reasons",
                "details": "Rejected applicants must receive specific explanations."
            })

    if rules["requires_model_card"] and not model_card_available:
        findings.append({
            "severity": "High",
            "rule_id": "MODEL-CARD",
            "finding": "Missing model card",
            "details": "This jurisdiction configuration expects documentation of assumptions, limitations, and monitoring."
        })

    if rules["requires_human_oversight"] and not human_oversight_available:
        findings.append({
            "severity": "High",
            "rule_id": "HUMAN-OVERSIGHT",
            "finding": "Missing human oversight",
            "details": "Human review is expected for high-impact automated credit decision systems."
        })

    if rules["requires_bias_testing"] and not bias_testing_completed:
        findings.append({
            "severity": "High",
            "rule_id": "BIAS-TESTING",
            "finding": "Bias testing not completed",
            "details": "Bias testing is part of the jurisdiction configuration."
        })

    if rules["requires_drift_monitoring"] and not drift_monitoring_available:
        findings.append({
            "severity": "Medium",
            "rule_id": "DRIFT-MONITORING",
            "finding": "Missing drift monitoring",
            "details": "Model performance and fairness may change over time."
        })

    if rules["high_risk_ai_classification"]:
        findings.append({
            "severity": "Info",
            "rule_id": "HEIGHTENED-AI-GOVERNANCE",
            "finding": "Heightened AI governance classification",
            "details": "Credit scoring is treated as requiring enhanced governance in this jurisdiction configuration."
        })

    if rules.get("requires_consumer_duty_outcome_monitoring"):
        findings.append({
            "severity": "Info",
            "rule_id": "UK-CONSUMER-DUTY-OUTCOMES",
            "finding": "Consumer Duty outcome monitoring",
            "details": "The UK configuration expects evidence that credit decisions are monitored for customer outcomes and remediated when needed."
        })

    high = sum(1 for f in findings if f["severity"] == "High")
    medium = sum(1 for f in findings if f["severity"] == "Medium")

    if high:
        status = "Non-compliant / High Risk"
    elif medium:
        status = "Review Required"
    else:
        status = "No major issues detected"

    return {
        "jurisdiction": jurisdiction,
        "regime": rules["regime"],
        "rule_version": rules["rule_version"],
        "last_reviewed": rules["last_reviewed"],
        "regulatory_philosophy": rules["regulatory_philosophy"],
        "sources": rules["sources"],
        "overall_status": status,
        "findings": findings,
        "group_results": group_results,
    }


def print_report(report: Dict[str, Any]) -> None:
    print("=" * 90)
    print(f"Jurisdiction: {report['jurisdiction']}")
    print(f"Regime: {report['regime']}")
    print(f"Rule version: {report['rule_version']} | Last reviewed: {report['last_reviewed']}")
    print(f"Philosophy: {report['regulatory_philosophy']}")
    print(f"Overall status: {report['overall_status']}")
    print("-" * 90)
    for source in report["sources"]:
        print(f"Source: {source['rule_id']} | {source['source_name']}")
        print(f"Operational test: {source['operational_test']}")
    print("-" * 90)
    if report["findings"]:
        for i, f in enumerate(report["findings"], 1):
            print(f"{i}. [{f['severity']}] {f['finding']} ({f['rule_id']})")
            print(f"   {f['details']}")
    else:
        print("No findings.")
    print("=" * 90)
