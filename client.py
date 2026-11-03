"""
Fractional Excretion of Sodium (FeNa) & Urea (FeUrea) Client.
Zero-mock pure Python standard library implementation.
Calculates renal tubular electrolyte handling, BUN/Creatinine ratio,
and discriminates prerenal volume depletion from intrinsic acute tubular necrosis (ATN).
"""

import math
from typing import Dict, Any, Optional


class RenalFractionalExcretionClient:
    """
    Computes FeNa, FeUrea, and renal hemodynamic indices to quantify hydration state,
    circulatory perfusion, and tubular reabsorptive competence.
    """

    def __init__(self):
        pass

    def evaluate_excretion(
        self,
        urine_sodium_mmol_l: float,
        plasma_sodium_mmol_l: float,
        urine_creatinine_mg_dl: float,
        plasma_creatinine_mg_dl: float,
        urine_urea_mg_dl: Optional[float] = None,
        plasma_urea_nitrogen_mg_dl: Optional[float] = None,
        on_diuretics: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates FeNa (and FeUrea if urea values are provided).
        All units:
          urine_sodium_mmol_l: mEq/L or mmol/L
          plasma_sodium_mmol_l: mEq/L or mmol/L
          urine_creatinine_mg_dl: mg/dL
          plasma_creatinine_mg_dl: mg/dL
          urine_urea_mg_dl: mg/dL (optional)
          plasma_urea_nitrogen_mg_dl: mg/dL (BUN, optional)
          on_diuretics: True if subject is actively receiving loop/thiazide diuretics.
        """
        if plasma_sodium_mmol_l <= 0 or urine_creatinine_mg_dl <= 0:
            raise ValueError("Plasma sodium and urine creatinine must be strictly positive.")
        if urine_sodium_mmol_l < 0 or plasma_creatinine_mg_dl <= 0:
            raise ValueError("Urine sodium must be non-negative and plasma creatinine positive.")

        # FeNa = (U_Na * P_Cr) / (P_Na * U_Cr) * 100%
        fena_pct = (urine_sodium_mmol_l * plasma_creatinine_mg_dl) / (plasma_sodium_mmol_l * urine_creatinine_mg_dl) * 100.0

        # FeUrea if provided: FeUrea = (U_Urea * P_Cr) / (P_Urea * U_Cr) * 100%
        feurea_pct = None
        if urine_urea_mg_dl is not None and plasma_urea_nitrogen_mg_dl is not None:
            if urine_urea_mg_dl > 0 and plasma_urea_nitrogen_mg_dl > 0:
                feurea_pct = (urine_urea_mg_dl * plasma_creatinine_mg_dl) / (plasma_urea_nitrogen_mg_dl * urine_creatinine_mg_dl) * 100.0

        # BUN / Creatinine ratio
        bun_cr_ratio = None
        if plasma_urea_nitrogen_mg_dl is not None:
            bun_cr_ratio = plasma_urea_nitrogen_mg_dl / plasma_creatinine_mg_dl

        # Clinical Classification Logic
        # Normal baseline physiological FeNa is typically ~0.5 - 1.0%
        if on_diuretics and feurea_pct is not None:
            primary_metric = "FeUrea (Diuretic-Adjusted)"
            if feurea_pct < 35.0:
                classification = "Prerenal Azotemia / Systemic Hypoperfusion"
                pathophysiology = "Avid proximal tubular urea reabsorption confirms hypovolemia despite natriuresis from diuretic therapy."
                hydration_status = "Dehydrated / Underfilled"
            elif feurea_pct > 50.0:
                classification = "Intrinsic Renal Impairment / Tubular Injury"
                pathophysiology = "Loss of tubular reabsorptive capacity (FeUrea > 50%) characteristic of acute tubular injury."
                hydration_status = "Normovolemic or Fluid Overloaded"
            else:
                classification = "Intermediate / Indeterminate Tubular Profile"
                pathophysiology = "Borderline urea reabsorption; correlation with clinical volume assessment recommended."
                hydration_status = "Equivocal"
        else:
            primary_metric = "FeNa"
            if fena_pct < 1.0:
                classification = "Prerenal Azotemia / Physiological Volume Depletion"
                pathophysiology = "Intact renal tubular conservation (FeNa < 1.0%) preserving sodium in response to low renal perfusion."
                hydration_status = "Dehydrated / Hypovolemic"
            elif fena_pct > 2.0:
                classification = "Intrinsic Renal / Acute Tubular Necrosis (ATN)"
                pathophysiology = "Impaired tubular epithelial sodium reabsorption leading to sodium wasting (FeNa > 2.0%)."
                hydration_status = "Euvolemic or Hypervolemic"
            else:
                classification = "Indeterminate / Early Transition Zone"
                pathophysiology = "FeNa between 1.0% and 2.0%; could represent mild tubular stress or postrenal obstruction."
                hydration_status = "Equivocal"

        return {
            "status": "success",
            "fena_percentage": round(fena_pct, 2),
            "feurea_percentage": round(feurea_pct, 2) if feurea_pct is not None else None,
            "bun_cr_ratio": round(bun_cr_ratio, 1) if bun_cr_ratio is not None else None,
            "primary_diagnostic_index": primary_metric,
            "evaluation": {
                "classification": classification,
                "hydration_status": hydration_status,
                "pathophysiology": pathophysiology,
                "diuretic_flag": on_diuretics
            }
        }
