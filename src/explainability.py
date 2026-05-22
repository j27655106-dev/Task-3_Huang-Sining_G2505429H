from __future__ import annotations

import pandas as pd
import numpy as np
from typing import Dict
from .model_pipeline import adverse_action_reasons, MODEL_FEATURES


def explain_rejections(df: pd.DataFrame, sample_size: int = 10) -> pd.DataFrame:
    """Create local adverse-action explanations for rejected applicants.

    This is not full SHAP, but it plays the same governance role in a simplified class prototype:
    translating model output into human-readable adverse action reasons.
    """
    rejected = df[df["approved"] == 0].copy().head(sample_size)
    if rejected.empty:
        return pd.DataFrame(columns=["applicant_id", "reason_1", "reason_2", "reason_3"])

    reasons = rejected.apply(adverse_action_reasons, axis=1)
    rows = []
    for applicant_id, reason_list in zip(rejected["applicant_id"], reasons):
        padded = list(reason_list) + [""] * (3 - len(reason_list))
        rows.append({
            "applicant_id": applicant_id,
            "reason_1": padded[0],
            "reason_2": padded[1],
            "reason_3": padded[2],
        })
    return pd.DataFrame(rows)


def feature_importance_from_logistic_model(pipeline) -> pd.DataFrame:
    """Approximate global explainability using logistic regression coefficients."""
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feature_names = []
    for name, transformer, cols in preprocessor.transformers_:
        if name == "cat":
            encoded = list(transformer.get_feature_names_out(cols))
            feature_names.extend(encoded)
        elif name == "num":
            feature_names.extend(cols)

    coefs = model.coef_[0]
    importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefs,
        "absolute_importance": np.abs(coefs)
    }).sort_values("absolute_importance", ascending=False)

    return importance


def shap_global_summary(pipeline, df: pd.DataFrame) -> dict:
    """Compute SHAP values for the logistic regression pipeline.

    Uses LinearExplainer on the transformed feature space. Returns raw SHAP
    values, transformed input matrix, and feature names for use in plots.
    The background dataset is the full transformed training set.
    """
    import shap

    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    X = df[MODEL_FEATURES]
    X_transformed = preprocessor.transform(X)

    feature_names = []
    for name, transformer, cols in preprocessor.transformers_:
        if name == "cat":
            feature_names.extend(list(transformer.get_feature_names_out(cols)))
        elif name == "num":
            feature_names.extend(cols)

    explainer = shap.LinearExplainer(model, X_transformed)
    shap_values = explainer.shap_values(X_transformed)

    return {
        "shap_values": shap_values,
        "X_transformed": X_transformed,
        "feature_names": feature_names,
        "explainer": explainer,
    }


def shap_local_explanation(pipeline, df: pd.DataFrame, applicant_idx: int) -> dict:
    """Return SHAP values for a single applicant (local explanation)."""
    result = shap_global_summary(pipeline, df)
    return {
        "shap_values_single": result["shap_values"][applicant_idx],
        "X_single": result["X_transformed"][applicant_idx],
        "feature_names": result["feature_names"],
        "expected_value": result["explainer"].expected_value,
    }
