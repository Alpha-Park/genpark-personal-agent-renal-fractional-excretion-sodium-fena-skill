# Renal Fractional Excretion of Sodium (FeNa) & Urea Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Renal Fractional Excretion of Sodium (FeNa) & Urea (FeUrea) Quantitative Evaluator. Differentiates systemic hypovolemia from intrinsic tubular injury with diuretic compensation.

```mermaid
flowchart TD
    A[Serum & Urine Chemistries: Na, Cr, Urea] --> B{Diuretic Therapy Active?}
    B -- No --> C[Compute FeNa = U_Na * P_Cr / P_Na * U_Cr * 100%]
    B -- Yes --> D[Compute FeUrea = U_Urea * P_Cr / P_Urea * U_Cr * 100%]
    C --> E{FeNa Threshold}
    E -- < 1.0% --> F[Prerenal Hypoperfusion / Dehydration]
    E -- > 2.0% --> G[Intrinsic Acute Tubular Necrosis]
    D --> H{FeUrea Threshold}
    H -- < 35% --> F
    H -- > 50% --> G
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Diuretic Compensation**: Automatically switches to FeUrea when diuretics confound urinary sodium handling.
- **Precision Nephrology**: Quantitative clearance formulas matching clinical nephrology guidelines.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
