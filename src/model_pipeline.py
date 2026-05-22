from __future__ import annotations

from typing import Dict, List, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MODEL_FEATURES = [
    "age", "annual_income", "credit_score", "loan_amount", "debt_to_income", "employment_status"
]

SENSITIVE_ATTRIBUTES = ["nationality", "ethnicity", "religion", "marital_status"]


def train_credit_model(df: pd.DataFrame, threshold: float = 0.35) -> Tuple[pd.DataFrame, Pipeline, Dict[str, float]]:
    X = df[MODEL_FEATURES]
    y = df["defaulted"]

    categorical_features = ["employment_status"]
    numeric_features = ["age", "annual_income", "credit_score", "loan_amount", "debt_to_income"]

    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ("num", StandardScaler(), numeric_features)
    ])

    model = LogisticRegression(max_iter=2000)
    pipeline = Pipeline([("preprocessor", preprocessor), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    pipeline.fit(X_train, y_train)

    scores = pipeline.predict_proba(X)[:, 1]
    approved = (scores < threshold).astype(int)

    out = df.copy()
    out["predicted_default_probability"] = scores
    out["approved"] = approved

    y_pred_test = pipeline.predict(X_test)
    y_score_test = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred_test)),
        "roc_auc": float(roc_auc_score(y_test, y_score_test)),
        "approval_rate": float(out["approved"].mean()),
        "decision_threshold": float(threshold),
    }
    return out, pipeline, metrics


def adverse_action_reasons(row: pd.Series) -> List[str]:
    reasons = []
    if row["credit_score"] < 640:
        reasons.append("Credit score below internal benchmark")
    if row["debt_to_income"] > 0.45:
        reasons.append("Debt-to-income ratio is high")
    if row["annual_income"] < 30000:
        reasons.append("Income below affordability benchmark")
    if row["employment_status"] in ["unemployed", "student"]:
        reasons.append("Employment status increases repayment uncertainty")
    if row["loan_amount"] > 30000:
        reasons.append("Requested loan amount is high relative to profile")
    if not reasons:
        reasons.append("Overall predicted default risk exceeds approval threshold")
    return reasons[:3]
