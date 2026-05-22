# Rule Source Map

This document links the prototype's operational rules to regulatory sources and public materials used for the assignment.

| Rule area | Jurisdiction | Source | Operationalisation in prototype |
|---|---|---|---|
| Adverse action explanation | US | CFPB guidance on AI-driven credit decisions | Generate human-readable rejection reasons |
| Fair lending outcome review | US | ECOA / Regulation B-style logic | Monitor approval disparity across protected/proxy groups |
| Consumer outcomes | UK | FCA Consumer Duty outcome monitoring | Use stricter review threshold and require board-level outcome evidence |
| Responsible lending governance | UK | FCA Consumer Duty implementation planning | Require documentation, monitoring, human oversight, and remediation logic |
| Model risk management | US/UK governance layer | OCC model risk management principles used as a general lifecycle reference | Add model card, drift simulation, and monitoring outputs |
| Rule versioning | US/UK governance layer | Assignment requirement to show jurisdiction configuration | Store rule version and last-reviewed date in `src/config_rules.py` and include them in the generated compliance report |

The prototype does not claim to implement the full law. It translates selected regulatory expectations into operational checks for demonstration.
