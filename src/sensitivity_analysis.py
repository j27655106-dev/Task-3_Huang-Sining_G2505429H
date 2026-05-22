from __future__ import annotations

import pandas as pd
from .model_pipeline import train_credit_model
from .compliance_checker import disparity_ratio


def run_threshold_sensitivity(df: pd.DataFrame, thresholds=None) -> pd.DataFrame:
    if thresholds is None:
        thresholds = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60]

    rows = []
    for t in thresholds:
        results, _, metrics = train_credit_model(df, threshold=t)
        rows.append({
            "threshold": t,
            "approval_rate": metrics["approval_rate"],
            "roc_auc": metrics["roc_auc"],
            "ethnicity_disparity_ratio": disparity_ratio(results, "ethnicity"),
            "religion_disparity_ratio": disparity_ratio(results, "religion"),
            "nationality_disparity_ratio": disparity_ratio(results, "nationality"),
        })
    return pd.DataFrame(rows)
