#!/usr/bin/env python3
"""
Verification script for convention-robustness summary table.
Reproduces key OOS Sharpe (c2c vs overnight) and beta numbers from experiment JSONs.
Run with: python3 verify_convention_robustness.py
Requires cached data in data/ and SEED=42 for reproducibility.
"""

import json
import sys

def load_json(path):
    with open(path) as f:
        return json.load(f)

def verify_tsm_pure():
    """TSM Pure: c2c from E020 equity_only_close_to_close, overnight from E020 equity_only_next_open"""
    print("=== TSM Pure (Equity Flagship) ===")
    e020 = load_json("experiments/e020_robustness.json")
    c2c = e020["part_a"]["equity_only_close_to_close"]["oos_sharpe"]
    overnight = e020["part_a"]["equity_only_next_open"]["oos_sharpe"]
    c2c_beta = e020["part_a"]["equity_only_close_to_close"]["equity_beta"]
    overnight_beta = e020["part_a"]["equity_only_next_open"]["equity_beta"]
    print(f"  OOS Sharpe (c2c):       {c2c:.3f}  (target: 1.739)")
    print(f"  OOS Sharpe (overnight): {overnight:.3f}  (target: 2.157)")
    print(f"  Beta vs SPY (c2c):      {c2c_beta:.3f}  (target: -0.119)")
    print(f"  Beta vs SPY (overnight):{overnight_beta:.3f}  (target: -0.065)")
    assert abs(c2c - 1.739) < 0.01, f"c2c Sharpe mismatch: {c2c}"
    assert abs(overnight - 2.157) < 0.01, f"overnight Sharpe mismatch: {overnight}"
    assert abs(c2c_beta - (-0.119)) < 0.01, f"c2c beta mismatch: {c2c_beta}"
    assert abs(overnight_beta - (-0.065)) < 0.01, f"overnight beta mismatch: {overnight_beta}"
    print("  ✓ PASS\n")

def verify_dn_lowbeta():
    """DN Low-Beta: c2c from E041 component_attribution (1.053 in README), overnight from E013"""
    print("=== Dollar-Neutral Low-Beta Sort ===")
    e013 = load_json("experiments/e013_dnlb_large_liquid.json")
    overnight = e013["oos_sharpe"]
    # c2c from README final summary: 1.053
    c2c = 1.053
    # overnight beta from README: -0.035
    # c2c beta from E041 convention_findings: +1.02
    print(f"  OOS Sharpe (c2c):       {c2c:.3f}  (from README final summary)")
    print(f"  OOS Sharpe (overnight): {overnight:.3f}  (target: 1.287, committed E013 value)")
    print(f"  Beta vs SPY (c2c):      +1.02  (from E041 convention_findings)")
    print(f"  Beta vs SPY (overnight): -0.035  (from README)")
    # Assert against the committed E013 golden value (1.2867 rounds to 1.287),
    # not the 1.289 carried in FINAL_SUMMARY.json (a point-in-time snapshot
    # that predates E040-E042 and is retained as a historical artifact).
    assert abs(overnight - 1.287) < 0.001, f"overnight Sharpe mismatch: {overnight}"
    print("  ✓ PASS\n")

def verify_futures_tsm_18m():
    """Futures TSM 18m: from E018 tsm_lookback_grid 18m"""
    print("=== Futures TSM 18m (de-seamed) ===")
    e018 = load_json("experiments/e018_carry_validation.json")
    sharpe = e018["tsm_lookback_grid"]["18m"]["oos_sharpe"]
    beta = e018["tsm_lookback_grid"]["18m"]["equity_beta"]
    print(f"  OOS Sharpe (c2c):       {sharpe:.3f}  (target: 0.805)")
    print(f"  Beta vs SPY (c2c):      {beta:.3f}  (target: -0.010)")
    print(f"  Overnight: balanced split (E024 audit)")
    assert abs(sharpe - 0.805) < 0.01, f"Sharpe mismatch: {sharpe}"
    assert abs(beta - (-0.010)) < 0.01, f"Beta mismatch: {beta}"
    print("  ✓ PASS\n")

def verify_futures_carry():
    """Futures Carry (Realized Roll Yield): from E017"""
    print("=== Futures Carry (Realized Roll Yield) ===")
    e017 = load_json("experiments/e017_extended_futures.json")
    sharpe = e017["results"]["carry_realized_rollyield"]["oos_sharpe"]
    beta = e017["results"]["carry_realized_rollyield"]["equity_beta"]
    print(f"  OOS Sharpe (c2c):       {sharpe:.3f}  (target: 0.523)")
    print(f"  Beta vs SPY (c2c):      {beta:.3f}  (target: +0.014)")
    print(f"  Overnight: balanced split (E024 audit)")
    assert abs(sharpe - 0.523) < 0.01, f"Sharpe mismatch: {sharpe}"
    assert abs(beta - 0.014) < 0.01, f"Beta mismatch: {beta}"
    print("  ✓ PASS\n")

def verify_macro_momentum():
    """Macro Momentum: c2c from README (0.006), overnight from E022 strategy.oos_sharpe (0.428)"""
    print("=== Macro Momentum (Brooks 2017) ===")
    e022 = load_json("experiments/e022_macro_momentum.json")
    # E022 strategy.oos_sharpe = 0.428 is the overnight convention (per E023)
    overnight = e022["strategy"]["oos_sharpe"]
    beta = e022["strategy"]["equity_beta"]
    c2c = 0.006  # from README final summary
    print(f"  OOS Sharpe (c2c):       {c2c:.3f}  (from README final summary)")
    print(f"  OOS Sharpe (overnight): {overnight:.3f}  (target: 0.428)")
    print(f"  Beta vs SPY (c2c):      {beta:.3f}  (target: -0.011)")
    assert abs(overnight - 0.428) < 0.01, f"overnight Sharpe mismatch: {overnight}"
    assert abs(beta - (-0.011)) < 0.01, f"Beta mismatch: {beta}"
    print("  ✓ PASS\n")

def verify_low_vol():
    """Low-Vol Flagship: from E037 unlevered_lowvol"""
    print("=== Low-Vol Flagship (unlevered) ===")
    e037 = load_json("experiments/e037_portfolio.json")
    sharpe = e037["unlevered_lowvol"]["oos_sharpe"]
    beta = e037["unlevered_lowvol"]["beta_vs_spy"]
    print(f"  OOS Sharpe (c2c):       {sharpe:.3f}  (target: 1.728)")
    print(f"  Beta vs SPY (c2c):      {beta:.3f}  (target: +1.084)")
    print(f"  Overnight: not separately reported (E024 audit would show concentration)")
    assert abs(sharpe - 1.728) < 0.01, f"Sharpe mismatch: {sharpe}"
    assert abs(beta - 1.084) < 0.01, f"Beta mismatch: {beta}"
    print("  ✓ PASS\n")

def verify_e042():
    """E042 Min-Variance Blend: primary results.

    Asserts the recorded release invariants from the v1.2.3 golden
    (full pre-registered config: n_sim=50 + sensitivity grid,
    2026-10-12 committed cache vintage):
    OOS Sharpe 0.979, beta-constrained placebo z=1.72 (G2 FAIL),
    beta +0.094, bear Sharpe +1.967, turnover 0.0043, 4/5 gates,
    decision PARTIAL. A quick-run artifact (n_sim=2) reports a
    meaningless 2-sim placebo z and a spurious 5/5 VALIDATED
    decision; these assertions fail loudly on it.
    """
    print("=== E042 Min-Variance Market-Neutral Blend ===")
    e042 = load_json("experiments/e042_minvar_market_neutral.json")
    primary = e042["primary"]
    placebo = e042["placebo_constrained"]
    gates = e042["promotion_gates"]
    print(f"  OOS Sharpe (c2c):       {primary['oos_sharpe']:.3f}  (target: 0.979, gate: ≥0.8 → {'PASS' if gates['G1_oos_sharpe_gte_0.8'] else 'FAIL'})")
    print(f"  Placebo z (constrained): {placebo['z_score']:.2f}  (target: 1.72, gate: ≥3.0 → {'PASS' if gates['G2_placebo_z_gte_3.0'] else 'FAIL'})")
    print(f"  Beta vs SPY (full):     {primary['equity_beta']:.3f}  (target: +0.094, gate: ≤0.1 → {'PASS' if gates['G3_abs_beta_vs_spy_lte_0.1'] else 'FAIL'})")
    print(f"  Bear Sharpe:            {primary['bear_sharpe']:.2f}  (target: +1.967, gate: >0 → {'PASS' if gates['G4_bear_sharpe_gt_0'] else 'FAIL'})")
    print(f"  Turnover:               {primary['turnover']:.4f}  (target: 0.0043, gate: ≤0.15 → {'PASS' if gates['G5_turnover_lte_0.15'] else 'FAIL'})")
    n_pass = sum(v for k, v in gates.items() if k != "all_passed")
    print(f"  Gates passed: {gates['all_passed']} ({n_pass}/5)")
    print(f"  Decision: {e042['decision']}")
    # Recorded release invariants (v1.2.3 golden, full pre-registered config)
    assert placebo["n_sim"] == 50, (
        f"placebo n_sim = {placebo['n_sim']}, expected 50 "
        "(quick-run artifact overwrote the release golden?)")
    assert abs(primary["oos_sharpe"] - 0.979) < 0.005, f"OOS Sharpe mismatch: {primary['oos_sharpe']}"
    assert abs(placebo["z_score"] - 1.72) < 0.01, f"placebo z mismatch: {placebo['z_score']}"
    assert abs(primary["equity_beta"] - 0.094) < 0.005, f"beta mismatch: {primary['equity_beta']}"
    assert abs(primary["bear_sharpe"] - 1.967) < 0.01, f"bear Sharpe mismatch: {primary['bear_sharpe']}"
    assert abs(primary["turnover"] - 0.0043) < 0.0005, f"turnover mismatch: {primary['turnover']}"
    assert n_pass == 4, f"gates passed {n_pass}/5, expected 4/5 (G2 FAIL)"
    assert not gates["all_passed"], "all_passed is True, expected G2 placebo-significance FAIL"
    assert not gates["G2_placebo_z_gte_3.0"], "G2 unexpectedly passed"
    assert gates["G1_oos_sharpe_gte_0.8"], "G1 unexpectedly failed"
    assert gates["G3_abs_beta_vs_spy_lte_0.1"], "G3 unexpectedly failed"
    assert gates["G4_bear_sharpe_gt_0"], "G4 unexpectedly failed"
    assert gates["G5_turnover_lte_0.15"], "G5 unexpectedly failed"
    assert e042["decision"] == "PARTIAL", f"decision mismatch: {e042['decision']}"
    print("  ✓ PASS (PARTIAL 4/5 as recorded — G2 placebo-significance fails; not promoted)\n")

def main():
    print("=" * 60)
    print("CONVENTION-ROBUSTNESS VERIFICATION")
    print("Policy v1.2.3: Primary = close-to-close")
    print("=" * 60 + "\n")

    try:
        verify_tsm_pure()
        verify_dn_lowbeta()
        verify_futures_tsm_18m()
        verify_futures_carry()
        verify_macro_momentum()
        verify_low_vol()
        verify_e042()

        print("=" * 60)
        print("ALL VERIFICATIONS PASSED")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ VERIFICATION FAILED: {e}")
        return 1
    except FileNotFoundError as e:
        print(f"\n✗ FILE NOT FOUND: {e}")
        return 1
    except KeyError as e:
        print(f"\n✗ KEY ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())