from pathlib import Path
import sys
import json

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from src.data_generator import generate_synthetic_applicants
from src.model_pipeline import train_credit_model
from src.explainability import explain_rejections, feature_importance_from_logistic_model
from src.compliance_checker import run_compliance_check, print_report
from src.sensitivity_analysis import run_threshold_sensitivity
from src.drift_simulation import simulate_recession_drift, compare_baseline_and_drift


def main():
    data_dir = PROJECT_ROOT / "data"
    outputs_dir = PROJECT_ROOT / "outputs"
    data_dir.mkdir(exist_ok=True)
    outputs_dir.mkdir(exist_ok=True)

    df = generate_synthetic_applicants(n=1500, seed=42, bias_scenario=True)
    df.to_csv(data_dir / "synthetic_applicants.csv", index=False)

    decision_threshold = 0.50
    results, model, metrics = train_credit_model(df, threshold=decision_threshold)
    results.to_csv(outputs_dir / "applicants_with_predictions.csv", index=False)

    print("\nModel metrics")
    for k, v in metrics.items():
        print(f"- {k}: {v:.4f}" if isinstance(v, float) else f"- {k}: {v}")

    explanations = explain_rejections(results, sample_size=15)
    explanations.to_csv(outputs_dir / "adverse_action_explanations.csv", index=False)

    feature_importance = feature_importance_from_logistic_model(model)
    feature_importance.to_csv(outputs_dir / "feature_importance.csv", index=False)

    sensitivity = run_threshold_sensitivity(df)
    sensitivity.to_csv(outputs_dir / "threshold_sensitivity.csv", index=False)

    drift_df = simulate_recession_drift(df)
    drift_comparison = compare_baseline_and_drift(df, drift_df, threshold=decision_threshold)
    drift_comparison.to_csv(outputs_dir / "drift_comparison.csv", index=False)

    print("\nUS compliance report")
    us_report = run_compliance_check(
        results,
        jurisdiction="US",
        model_card_available=True,
        human_oversight_available=False,
        bias_testing_completed=True,
        drift_monitoring_available=True,
    )
    print_report(us_report)

    print("\nUK compliance report")
    uk_report = run_compliance_check(
        results,
        jurisdiction="UK",
        model_card_available=True,
        human_oversight_available=True,
        bias_testing_completed=True,
        drift_monitoring_available=True,
    )
    print_report(uk_report)

    with open(outputs_dir / "compliance_reports.json", "w", encoding="utf-8") as f:
        json.dump({"US": us_report, "UK": uk_report}, f, indent=2)

    print("\nGenerated output files in /outputs:")
    for path in outputs_dir.glob("*"):
        print(f"- {path.name}")


if __name__ == "__main__":
    main()
