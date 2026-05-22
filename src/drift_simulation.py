from __future__ import annotations

import numpy as np
import pandas as pd
from .model_pipeline import train_credit_model, MODEL_FEATURES
from .compliance_checker import disparity_ratio


def simulate_recession_drift(baseline_df: pd.DataFrame) -> pd.DataFrame:
    """Apply a recession-like income shock to the same baseline population.

    Income is reduced by 12% and debt-to-income inflated by 18%, simulating
    a macroeconomic shock applied to the identical applicant cohort. Using the
    same population isolates the effect of the shock from random seed variation.
    """
    df = baseline_df.copy()
    df["annual_income"] = (df["annual_income"] * 0.88).round(2)
    df["debt_to_income"] = (df["debt_to_income"] * 1.18).clip(0.02, 0.95).round(3)
    return df


def compare_baseline_and_drift(
    baseline_df: pd.DataFrame,
    drift_df: pd.DataFrame,
    threshold: float = 0.35,
) -> pd.DataFrame:
    """Compare compliance metrics under baseline and drift scenarios.

    The model is trained on baseline data and then applied unchanged to the
    drift data — simulating the real-world situation where an existing deployed
    model encounters a shifted applicant population. This isolates model drift
    from model retraining and reflects the regulatory concern: a previously
    validated model may produce different fairness outcomes as conditions change.
    """
    base_results, base_model, base_metrics = train_credit_model(baseline_df, threshold=threshold)

    # Apply baseline-trained model to drift population (no retraining)
    drift_scores = base_model.predict_proba(drift_df[MODEL_FEATURES])[:, 1]
    drift_approved = (drift_scores < threshold).astype(int)
    drift_results = drift_df.copy()
    drift_results["predicted_default_probability"] = drift_scores
    drift_results["approved"] = drift_approved
    drift_approval_rate = float(drift_approved.mean())

    return pd.DataFrame([
        {
            "scenario": "baseline",
            "approval_rate": base_metrics["approval_rate"],
            "roc_auc": base_metrics["roc_auc"],
            "ethnicity_disparity_ratio": disparity_ratio(base_results, "ethnicity"),
            "religion_disparity_ratio": disparity_ratio(base_results, "religion"),
        },
        {
            "scenario": "recession_drift",
            "approval_rate": drift_approval_rate,
            "roc_auc": float("nan"),
            "ethnicity_disparity_ratio": disparity_ratio(drift_results, "ethnicity"),
            "religion_disparity_ratio": disparity_ratio(drift_results, "religion"),
        },
    ])
