---
name: genpark-personal-agent-renal-fractional-excretion-sodium-fena-skill
description: Fractional Excretion of Sodium (FeNa) & Urea (FeUrea) quantitative analyzer. Differentiates prerenal hypoperfusion from acute tubular injury and resolves diuretic confounding.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - nephrology
  - hydration
  - fena
  - feurea
  - openclaw
  - genpark
  - mcp
---

# Renal Fractional Excretion of Sodium (FeNa) & Urea (FeUrea) Skill

## Overview
This skill computes the percentage of filtered sodium and urea excreted in the urine relative to creatinine clearance.
- **FeNa < 1.0%**: Suggests intact tubular function avidly reabsorbing sodium in response to decreased renal blood flow (prerenal azotemia, hypovolemia, dehydration).
- **FeNa > 2.0%**: Indicates tubular epithelial cell injury with loss of concentrating and reabsorptive ability (acute tubular necrosis, intrinsic renal failure).
- **Diuretic Adjustment (FeUrea)**: In patients on loop or thiazide diuretics, sodium excretion is artificially increased. Fractional Excretion of Urea (`FeUrea < 35%`) reliably unmasks prerenal pathophysiology.

## Mathematical Formulation
1. **Fractional Excretion of Sodium (FeNa)**:
   $$\text{FeNa} = \frac{U_{\text{Na}} \times P_{\text{Cr}}}{P_{\text{Na}} \times U_{\text{Cr}}} \times 100\%$$
2. **Fractional Excretion of Urea (FeUrea)**:
   $$\text{FeUrea} = \frac{U_{\text{Urea}} \times P_{\text{Cr}}}{P_{\text{Urea}} \times U_{\text{Cr}}} \times 100\%$$
3. **BUN / Creatinine Ratio**:
   $$\text{Ratio} = \frac{\text{BUN}}{\text{Plasma Creatinine}}$$

## Usage
```python
from client import RenalFractionalExcretionClient

client = RenalFractionalExcretionClient()
res = client.evaluate_excretion(
    urine_sodium_mmol_l=14.0,
    plasma_sodium_mmol_l=139.0,
    urine_creatinine_mg_dl=130.0,
    plasma_creatinine_mg_dl=1.8
)
print(res["evaluation"]["classification"])
```
