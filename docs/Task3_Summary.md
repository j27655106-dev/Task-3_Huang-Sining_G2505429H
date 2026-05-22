# Task 3 Summary

## Plain-Language Design Summary

This project implements a jurisdiction-aware RegTech prototype for AI-driven credit scoring. It is designed for a Lendable / Zable-style consumer credit platform operating across the United States and the United Kingdom.

The tool uses synthetic applicant data to train a simplified credit risk model. Sensitive attributes are excluded from training but retained for fairness auditing. This means the model does not directly use protected characteristics, while the compliance layer can still test whether outcomes differ by group.

The same model output is evaluated under two regulatory configurations. The US configuration emphasizes fair lending outcomes and adverse action explanations. The UK configuration emphasizes FCA Consumer Duty-style outcome monitoring, responsible lending governance, documentation, human oversight, and remediation evidence.

In the demo run, the same portfolio receives different compliance meanings. Under the US configuration, no major issue is detected because the approval disparity ratios clear the US threshold. Under the UK configuration, the same results require review because the UK threshold is stricter and the system must be monitored for customer outcomes.

## Why This Product Is Right for the Company

The hypothetical company sells practical compliance automation to mid-sized lenders that cannot maintain separate manual compliance teams for every jurisdiction. Its strength is translating regulatory expectations into configurable operational checks. A jurisdiction-aware credit compliance module fits that strategy because AI lending creates repeatable monitoring needs across markets.

## Why a Tool Is Better Than a Memo or Spreadsheet

A memo can describe regulatory differences, but it cannot rerun the checks when data, thresholds, or rules change. A spreadsheet can track individual metrics, but it is weak at preserving rule versions, model assumptions, adverse action explanations, and drift evidence in one repeatable workflow. This prototype turns those elements into executable checks.

## Regulatory Divergence Handled

The tool handles the divergence between US fair lending and Regulation B-style explanation logic, and UK FCA Consumer Duty-style outcome monitoring. The operational difference is not cosmetic: the same approval-rate disparity can pass the US configuration but trigger UK review because the UK setup applies stricter outcome monitoring and governance controls.

## What the Tool Does Not Do

The tool does not provide legal advice, decide whether unlawful discrimination occurred, or replace human judgement. It also does not use real customer data. These boundaries are deliberate because the assignment prototype should demonstrate regulatory mechanics without pretending to be a production legal determination system.
