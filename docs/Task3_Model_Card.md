# Task 3 Model Card

## Model purpose
The model simulates an AI credit scoring system used to estimate default probability and automate approval decisions.

## Intended use
This model is used only for a class prototype. It demonstrates how a RegTech tool can evaluate the same AI model under different US and UK jurisdictional assumptions.

## Inputs used by the model
- age
- annual income
- credit score
- loan amount
- debt-to-income ratio
- employment status

## Sensitive attributes excluded from training
- nationality
- ethnicity
- religion
- marital status

These attributes are retained for fairness auditing only.

## Explainability
The prototype generates adverse action reasons for rejected applicants and produces coefficient-based global feature importance from the logistic regression model.

## Governance controls
- jurisdiction configuration layer
- bias testing
- adverse action explanation
- sensitivity analysis
- drift simulation
- model card

## Key assumptions
- Data is synthetic and does not represent real applicants.
- Legal thresholds are illustrative.
- The tool flags risk; it does not determine legal liability.
- Human judgement is required for high-severity findings.

## Failure modes
- False positive: over-flagging may reduce lending access.
- False negative: hidden bias may persist.
- Drift: economic or applicant distribution shifts may alter fairness outcomes.
- Jurisdiction misconfiguration: applying US logic to UK deployment, or vice versa.
- False sense of compliance: the most serious failure, where risk persists while appearing documented.
