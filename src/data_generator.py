from __future__ import annotations

import numpy as np
import pandas as pd


def generate_synthetic_applicants(n: int = 1500, seed: int = 42, bias_scenario: bool = True) -> pd.DataFrame:
    """Generate synthetic credit applicants.

    Sensitive attributes are generated for fairness auditing but are not used in model training.
    bias_scenario=True introduces realistic correlation between socioeconomic variables and group labels,
    representing inherited structural patterns rather than direct use of protected variables.
    """
    rng = np.random.default_rng(seed)

    df = pd.DataFrame({
        "applicant_id": np.arange(1, n + 1),
        "nationality": rng.choice(["US", "UK", "Germany", "France", "Singapore", "Canada", "India", "China"], n,
                                  p=[0.32, 0.10, 0.10, 0.08, 0.08, 0.08, 0.12, 0.12]),
        "ethnicity": rng.choice(["Group_A", "Group_B", "Group_C", "Group_D"], n,
                                p=[0.50, 0.25, 0.15, 0.10]),
        "religion": rng.choice(["Religion_A", "Religion_B", "Religion_C", "None/Not disclosed"], n,
                               p=[0.30, 0.25, 0.20, 0.25]),
        "marital_status": rng.choice(["single", "married", "divorced", "widowed"], n,
                                     p=[0.45, 0.42, 0.10, 0.03]),
        "employment_status": rng.choice(["full_time", "part_time", "self_employed", "unemployed", "student"], n,
                                        p=[0.55, 0.12, 0.17, 0.08, 0.08]),
    })

    df["age"] = np.clip(rng.normal(38, 12, n).round(), 18, 75).astype(int)

    income_base = {
        "full_time": 78000,
        "part_time": 39000,
        "self_employed": 65000,
        "unemployed": 22000,
        "student": 18000,
    }

    income = np.array([rng.normal(income_base[s], income_base[s] * 0.35) for s in df["employment_status"]])

    if bias_scenario:
        # Indirect structural correlation: some groups have lower generated income / credit score distribution.
        income -= np.where(df["ethnicity"].isin(["Group_C", "Group_D"]), rng.normal(6000, 2000, n), 0)
        income -= np.where(df["religion"].isin(["Religion_C"]), rng.normal(2500, 1200, n), 0)

    df["annual_income"] = np.maximum(8000, income).round(2)

    credit_score = rng.normal(670, 75, n)
    if bias_scenario:
        credit_score -= np.where(df["ethnicity"].isin(["Group_D"]), rng.normal(25, 10, n), 0)
        credit_score -= np.where(df["employment_status"].isin(["unemployed", "student"]), rng.normal(20, 8, n), 0)

    df["credit_score"] = np.clip(credit_score, 300, 850).round().astype(int)
    df["loan_amount"] = np.clip(rng.normal(18000, 9000, n), 1000, 60000).round(2)
    df["debt_to_income"] = np.clip(rng.beta(2, 5, n), 0.02, 0.95).round(3)

    # Default probability uses only financial variables and employment status.
    # The coefficients are intentionally centred so the synthetic portfolio has
    # a plausible mix of approvals and rejections instead of a saturated outcome.
    logit = (
        -1.25
        + 0.000045 * (df["loan_amount"] - 18000)
        - 0.000018 * (df["annual_income"] - 65000)
        - 0.012 * (df["credit_score"] - 660)
        + 2.4 * (df["debt_to_income"] - 0.30)
        + (df["employment_status"].isin(["unemployed", "student"]).astype(int) * 0.9)
    )
    probability_default = 1 / (1 + np.exp(-logit))
    df["default_probability_true"] = np.clip(probability_default, 0.02, 0.92)
    df["defaulted"] = rng.binomial(1, df["default_probability_true"])

    return df
