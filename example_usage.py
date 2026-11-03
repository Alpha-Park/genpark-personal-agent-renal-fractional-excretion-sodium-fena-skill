"""
Example usage of Renal Fractional Excretion of Sodium (FeNa) & Urea Skill.
Demonstrates prerenal hypoperfusion vs acute tubular necrosis (ATN) and diuretic confounding.
"""

import json
from client import RenalFractionalExcretionClient


def main():
    print("=== Testing Renal Fractional Excretion (FeNa / FeUrea) Skill ===")
    client = RenalFractionalExcretionClient()

    # 1. Prerenal azotemia / severe dehydration (avid sodium reabsorption: U_Na=15, P_Na=140, U_Cr=120, P_Cr=2.0)
    res_prerenal = client.evaluate_excretion(
        urine_sodium_mmol_l=15.0,
        plasma_sodium_mmol_l=140.0,
        urine_creatinine_mg_dl=120.0,
        plasma_creatinine_mg_dl=2.0,
        urine_urea_mg_dl=400.0,
        plasma_urea_nitrogen_mg_dl=50.0,
        on_diuretics=False
    )
    print("\n[Case 1: Prerenal Hypoperfusion / Dehydration]")
    print(json.dumps(res_prerenal, indent=2))

    # 2. Acute Tubular Necrosis (ATN) (sodium wasting: U_Na=65, P_Na=138, U_Cr=40, P_Cr=2.8)
    res_atn = client.evaluate_excretion(
        urine_sodium_mmol_l=65.0,
        plasma_sodium_mmol_l=138.0,
        urine_creatinine_mg_dl=40.0,
        plasma_creatinine_mg_dl=2.8,
        on_diuretics=False
    )
    print("\n[Case 2: Acute Tubular Necrosis - Sodium Wasting]")
    print(json.dumps(res_atn, indent=2))

    # 3. Patient on Furosemide (Loop diuretic elevates FeNa, but FeUrea remains low < 35%)
    res_diuretic = client.evaluate_excretion(
        urine_sodium_mmol_l=45.0,
        plasma_sodium_mmol_l=136.0,
        urine_creatinine_mg_dl=60.0,
        plasma_creatinine_mg_dl=2.2,
        urine_urea_mg_dl=280.0,
        plasma_urea_nitrogen_mg_dl=48.0,
        on_diuretics=True
    )
    print("\n[Case 3: Diuretic Patient - FeUrea Used for Diagnosis]")
    print(json.dumps(res_diuretic, indent=2))

    # Assertions
    assert res_prerenal["fena_percentage"] < 1.0
    assert res_atn["fena_percentage"] > 2.0
    assert res_diuretic["evaluation"]["diuretic_flag"] is True
    print("\n[SUCCESS] All Renal Fractional Excretion test cases passed!")


if __name__ == "__main__":
    main()
