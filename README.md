# Task 3: Jurisdiction-Aware AI Credit Fairness Checker

Huang Sining  
G2505429H  
SINING001@e.ntu.edu.sg

## Project Overview

This repository contains a working prototype for Assignment 1 Task 3.

The project designs and partially implements a jurisdiction-aware RegTech tool for AI-driven credit scoring. The prototype is built around a Lendable / Zable-style consumer credit platform and compares compliance expectations in the United States and the United Kingdom.

The submission follows Option A (Working Prototype), with additional quantitative analysis elements from Option C:

- synthetic applicant data
- AI credit risk model
- jurisdiction configuration layer
- US vs UK compliance checks
- SHAP explainability (global summary + local waterfall) and adverse action reasons
- sensitivity analysis
- drift simulation (baseline model applied to income-shocked population)
- model card and governance documentation stub
- data collaboration note

## Key Regulatory Idea

The same credit scoring model can produce the same technical output while creating different compliance meanings across jurisdictions.

- United States: fair lending outcomes, adverse action reasons, and Regulation B-style explanation logic
- United Kingdom: FCA Consumer Duty-style outcome monitoring, responsible lending governance, documentation, human oversight, and remediation evidence

In the current demo run, the same synthetic portfolio is not flagged as a major US issue, but it is marked as requiring UK review because the UK configuration applies a stricter approval-disparity threshold and Consumer Duty outcome-monitoring expectation.

## Repository Structure

```text
Task3_Jurisdiction_Aware_Credit_Compliance_Tool/
|-- README.md
|-- requirements.txt
|-- run_demo.py
|-- data/
|   `-- synthetic_applicants.csv
|-- outputs/
|   |-- applicants_with_predictions.csv
|   |-- adverse_action_explanations.csv
|   |-- feature_importance.csv
|   |-- threshold_sensitivity.csv
|   |-- drift_comparison.csv
|   `-- compliance_reports.json
|-- notebooks/
|   `-- Task3_Prototype_APlus.ipynb   (pre-run with outputs)
|-- src/
|   |-- config_rules.py               (jurisdiction configuration layer)
|   |-- data_generator.py
|   |-- model_pipeline.py
|   |-- explainability.py             (SHAP + coefficient + adverse action)
|   |-- compliance_checker.py
|   |-- sensitivity_analysis.py
|   `-- drift_simulation.py
|-- docs/
|   |-- Task3_Model_Card.md
|   |-- Task3_Summary.md
|   |-- Task3_Tool_Design.pdf
|   |-- Task3_Data_Collaboration_Note.md
|   `-- Rule_Source_Map.md
`-- scripts/
    |-- generate_task1_pdf.py         (generates NTULearn Task1 PDF)
    |-- generate_task2_pdf.py         (generates NTULearn Task2 PDF)
    `-- generate_task3_pdf.py         (generates NTULearn Task3 PDF)
```

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full prototype:

```bash
python run_demo.py
```

Or open the notebook:

```bash
jupyter notebook notebooks/Task3_Prototype_APlus.ipynb
```

## Output Files

Running `python run_demo.py` regenerates:

- `outputs/applicants_with_predictions.csv`
- `outputs/adverse_action_explanations.csv`
- `outputs/feature_importance.csv`
- `outputs/threshold_sensitivity.csv`
- `outputs/drift_comparison.csv`
- `outputs/compliance_reports.json`

## Important Boundary

Sensitive demographic attributes are included for fairness auditing only. They are deliberately excluded from model training.

The tool is not legal advice and does not determine whether discrimination has occurred. It flags risk and governance gaps for human review.
