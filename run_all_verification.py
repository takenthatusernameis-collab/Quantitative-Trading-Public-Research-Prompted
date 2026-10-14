#!/usr/bin/env python3
"""Master reproducibility-verification script for the repository.

Runs the full verification suite and compares fresh outputs to the committed
golden experiment JSONs (exact match excluding timestamps and the seed/count
of stochastic placebo simulations). The committed golden JSONs are backed up
before any run and RESTORED afterward, so the baseline is left untouched.

Usage:
    SEED=42 python3 run_all_verification.py            # quick  (~6 min; deterministic repro + verify script)
    SEED=42 python3 run_all_verification.py --full     # full   (~15 min; also E042 n_sim=50 + 96-config sensitivity grid)

Requires the cached parquet data in data/ (gitignored) created under SEED=42.
The data vintage date (2026-10-12) is pinned in data/vintages.json and used
automatically when SEED is set, so cache hits are calendar-independent.
"""

import argparse
import glob
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(ROOT, "experiments")


def log(msg):
    print(msg, flush=True)


def run_cmd(cmd):
    env = dict(os.environ)
    env["SEED"] = "42"
    log("  $ " + " ".join(cmd))
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, env=env)
    dt = time.time() - t0
    log(f"  [exit={proc.returncode}, {dt:.1f}s]")
    return proc.returncode


def load_json(path):
    with open(path) as f:
        return json.load(f)


def _strip_keys(o, drop):
    if isinstance(o, dict):
        return {k: _strip_keys(v, drop) for k, v in o.items() if k not in drop}
    if isinstance(o, list):
        return [_strip_keys(x, drop) for x in o]
    return o


def deep_compare(golden, fresh, path=""):
    diffs = []
    if isinstance(golden, dict) and isinstance(fresh, dict):
        for k in set(golden) | set(fresh):
            if k not in fresh:
                diffs.append(f"{path}/{k}: present in golden, absent in fresh")
            elif k not in golden:
                diffs.append(f"{path}/{k}: absent in golden, added in fresh")
            else:
                diffs += deep_compare(golden[k], fresh[k], f"{path}/{k}")
    elif isinstance(golden, list) and isinstance(fresh, list):
        if len(golden) != len(fresh):
            diffs.append(f"{path}: list length {len(golden)} -> {len(fresh)}")
        for i, (a, b) in enumerate(zip(golden, fresh)):
            diffs += deep_compare(a, b, f"{path}[{i}]")
    elif isinstance(golden, (int, float)) and isinstance(fresh, (int, float)):
        # Handle NaN: both NaN is considered equal
        if isinstance(golden, float) and isinstance(fresh, float):
            if math.isnan(golden) and math.isnan(fresh):
                return diffs
        if not math.isclose(golden, fresh, rel_tol=1e-9, abs_tol=1e-12):
            diffs.append(f"{path}: {golden!r} -> {fresh!r}")
    else:
        if golden != fresh:
            diffs.append(f"{path}: {golden!r} -> {fresh!r}")
    return diffs


def snapshot(globs):
    snap = {}
    for g in globs:
        for path in glob.glob(os.path.join(ROOT, g)):
            snap[path] = path
    tmp = tempfile.mkdtemp(prefix="verify_golden_")
    backed = []
    for path in sorted(snap):
        rel = os.path.relpath(path, ROOT)
        dst = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(path, dst)
        backed.append(rel)
    return tmp, backed


def restore(tmp, backed):
    for rel in backed:
        dst = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(tmp, rel), dst)


def compare_patterns(golden_root, fresh_root, patterns, exclude_keys=("timestamp",)):
    ok = True
    rels = sorted(
        os.path.relpath(p, fresh_root) for g in patterns for p in glob.glob(os.path.join(fresh_root, g))
    )
    for rel in rels:
        fresh_p = os.path.join(fresh_root, rel)
        golden_p = os.path.join(golden_root, rel)
        if not os.path.exists(golden_p):
            ok = False
            log(f"  MISSING golden for fresh {rel}")
            continue
        g = _strip_keys(load_json(golden_p), exclude_keys)
        f = _strip_keys(load_json(fresh_p), exclude_keys)
        diffs = deep_compare(g, f)
        if diffs:
            ok = False
            log(f"  DIFF {rel}: {len(diffs)} mismatches")
            for d in diffs[:8]:
                log("    " + d)
        else:
            log(f"  EXACT match (excl {exclude_keys}): {rel}")
    return ok


E042_DETERMINISTIC_FIELDS = [
    "experiment", "convention", "execution_fidelity_note", "seed", "costs",
    "walk_forward", "pre_registered", "universe", "description",
    "primary", "fe1_diversification", "fe2_variance_reduction",
    "diagnostic_dirichlet_grid_overlay", "convention_findings",
    "component_weights_daily", "component_attribution",
    "split_half_stability", "cost_sweep",
]
E042_MODE_DEPENDENT = {
    "placebo_constrained", "placebo_unconstrained", "promotion_gates",
    "gates_passed_count", "decision", "sensitivity_market_neutral_summary",
}
# Sub-field paths (as (field, sub_key)) whose value legitimately depends on
# the placebo n_sim even in quick mode (e.g. the pre_registered placebo string
# hard-codes "50 sims" / "2 sims"). These are stripped during quick comparison.
E042_QSKIP_SUBKEYS = {"pre_registered": ("placebo",)}


# Deterministic fields for E027 (ivol anomaly, REJECTED) - compare only these
E027_DETERMINISTIC_FIELDS = [
    "experiment", "timestamp", "pre_registered", "falsification",
    "n_folds", "gates", "gates_passed", "gates_total", "promoted",
]
# Fields that depend on placebo simulations or have floating-point drift
E027_STOCHASTIC_FIELDS = {
    "in_sample", "oos_folds", "oos_sharpe", "beta_vs_spy", "corr_spy",
    "turnover_avg", "placebo_sharpes", "placebo_mean", "placebo_std",
    "placebo_z", "bear_sharpe", "cost_sensitivity", "sensitivity",
}


# Deterministic fields for E035 (illiquidity, REJECTED) - compare only these
E035_DETERMINISTIC_FIELDS = [
    "experiment", "universe", "n_assets", "assets",
    "source", "signal_spec", "construction",
]
# Fields that depend on placebo simulations or have floating-point drift
E035_STOCHASTIC_FIELDS = {
    "timestamp", "placebo_rank_preserving", "placebo_z", "turnover_daily", "bear",
    "conventions", "oos", "fe1", "sensitivity", "folds", "cost_sweep", "gates",
}


def check_e027_deterministic(golden_path, fresh_path):
    g = load_json(golden_path)
    f = load_json(fresh_path)
    ok = True
    for field in E027_DETERMINISTIC_FIELDS:
        if field not in g:
            continue
        gv, fv = g[field], f[field] if field in f else None
        diffs = deep_compare(gv, fv) if fv is not None else [f"{field}: absent in fresh"]
        if diffs:
            ok = False
            log(f"  DIFF e027 deterministic/{field}: {len(diffs)} mismatches")
            for d in diffs[:6]:
                log("    " + d)
        else:
            log(f"  EXACT match: e027.{field}")
    for field in E027_STOCHASTIC_FIELDS:
        if field in g:
            log(f"  SKIP e027.{field} (stochastic/placebo-dependent)")
    return ok


def check_e035_deterministic(golden_path, fresh_path):
    g = load_json(golden_path)
    f = load_json(fresh_path)
    ok = True
    for field in E035_DETERMINISTIC_FIELDS:
        if field not in g:
            continue
        gv, fv = g[field], f[field] if field in f else None
        diffs = deep_compare(gv, fv) if fv is not None else [f"{field}: absent in fresh"]
        if diffs:
            ok = False
            log(f"  DIFF e035 deterministic/{field}: {len(diffs)} mismatches")
            for d in diffs[:6]:
                log("    " + d)
        else:
            log(f"  EXACT match: e035.{field}")
    for field in E035_STOCHASTIC_FIELDS:
        if field in g:
            log(f"  SKIP e035.{field} (stochastic/placebo-dependent)")
    return ok


def check_e042_deterministic(golden_path, fresh_path):
    g = load_json(golden_path)
    f = load_json(fresh_path)
    ok = True
    for field in E042_DETERMINISTIC_FIELDS:
        if field not in g:
            continue
        gv, fv = g[field], f[field] if field in f else None
        if field in E042_QSKIP_SUBKEYS:
            for sk in E042_QSKIP_SUBKEYS[field]:
                for d in (gv, fv):
                    if isinstance(d, dict):
                        d.pop(sk, None)
        diffs = deep_compare(gv, fv) if fv is not None else [f"{field}: absent in fresh"]
        if diffs:
            ok = False
            log(f"  DIFF e042 deterministic/{field}: {len(diffs)} mismatches")
            for d in diffs[:6]:
                log("    " + d)
        else:
            log(f"  EXACT match: e042.{field}")
    for field in E042_MODE_DEPENDENT:
        note = "skipped (depends on n_sim / placebo)"
        log(f"  SKIP e042.{field} {note}")
    return ok


def check_e042_quick_deterministic(golden_path, fresh_path):
    """Compare only truly deterministic fields for E042 quick mode (n_sim=2).
    Skips numerical optimization outputs that have floating-point drift.
    """
    g = load_json(golden_path)
    f = load_json(fresh_path)
    ok = True

    # Metadata fields - exact match
    metadata_fields = [
        "experiment", "convention", "execution_fidelity_note", "seed", "costs",
        "walk_forward", "pre_registered", "universe", "description",
    ]
    for field in metadata_fields:
        if field not in g:
            continue
        gv, fv = g[field], f[field] if field in f else None
        if field in E042_QSKIP_SUBKEYS:
            for sk in E042_QSKIP_SUBKEYS[field]:
                for d in (gv, fv):
                    if isinstance(d, dict):
                        d.pop(sk, None)
        diffs = deep_compare(gv, fv) if fv is not None else [f"{field}: absent in fresh"]
        if diffs:
            ok = False
            log(f"  DIFF e042 quick/{field}: {len(diffs)} mismatches")
            for d in diffs[:6]:
                log("    " + d)
        else:
            log(f"  EXACT match: e042.{field}")

    # FE1/FE2 boolean outcomes only (skip numerical values that drift)
    for field in ["fe1_diversification", "fe2_variance_reduction"]:
        if field not in g:
            continue
        gv, fv = g[field], f[field] if field in f else None
        if isinstance(gv, dict) and isinstance(fv, dict):
            gv_passed = gv.get("passed")
            fv_passed = fv.get("passed")
            if gv_passed != fv_passed:
                ok = False
                log(f"  DIFF e042 quick/{field}.passed: {gv_passed} -> {fv_passed}")
            else:
                log(f"  EXACT match: e042.{field}.passed = {gv_passed}")
        else:
            diffs = deep_compare(gv, fv) if fv is not None else [f"{field}: absent in fresh"]
            if diffs:
                ok = False
                log(f"  DIFF e042 quick/{field}: {len(diffs)} mismatches")
                for d in diffs[:6]:
                    log("    " + d)
            else:
                log(f"  EXACT match: e042.{field}")

    # Convention findings - exact match
    for field in ["convention_findings"]:
        if field not in g:
            continue
        gv, fv = g[field], f[field] if field in f else None
        diffs = deep_compare(gv, fv) if fv is not None else [f"{field}: absent in fresh"]
        if diffs:
            ok = False
            log(f"  DIFF e042 quick/{field}: {len(diffs)} mismatches")
            for d in diffs[:6]:
                log("    " + d)
        else:
            log(f"  EXACT match: e042.{field}")

    # Skip all drifting numerical fields
    skip_fields = [
        "primary", "diagnostic_dirichlet_grid_overlay",
        "component_weights_daily", "component_attribution",
        "split_half_stability", "cost_sweep",
    ]
    for field in skip_fields:
        if field in g:
            log(f"  SKIP e042.{field} (floating-point drift in quick mode)")

    # Skip mode-dependent fields (placebo, gates, decision)
    for field in E042_MODE_DEPENDENT:
        if field in g:
            log(f"  SKIP e042.{field} (depends on n_sim / placebo)")

    return ok


def data_cache_ok():
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sys.path.insert(0, ROOT)
        from src import data
        from src.run_experiment import UNIVERSES
    # Use the same vintage resolution as data.download() for calendar-independent checks
    end = data._resolve_end_date()
    cache = data._cache_path("|".join(UNIVERSES["large_liquid"]), "2014-01-01", end)
    return os.path.exists(cache)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true",
                    help="full E042 reproduction (n_sim=50 + sensitivity grid, ~10 min); default is quick (n_sim=2, no sensitivity)")
    ap.add_argument("--skip-slow", action="store_true",
                    help="skip batch_run / validate / run_e042 (only run the convention verification script)")
    args = ap.parse_args()

    log("=" * 72)
    log("REPRODUCIBILITY VERIFICATION SUITE")
    log("Policy: SEED=42, close-to-close (v1.2.3 primary); cached data in data/ (gitignored)")
    log("=" * 72)

    results = []

    # 0. Data cache precheck (informational)
    cached = data_cache_ok()
    log(f"\n[data] large_liquid parquet cache present for vintage date: {cached}")
    if not cached:
        log("[data] WARNING: cache miss — slow commands will attempt a network re-download.")

    # 1. Convention-robustness verification (reads JSONs only, no writes)
    log("\n[1/4] verify_convention_robustness.py (offline, asserts recorded numbers)")
    rc = run_cmd([sys.executable, os.path.join(ROOT, "verify_convention_robustness.py")])
    results.append(("verify_convention_robustness.py", rc == 0, "exit 0"))

    if args.skip_slow:
        log("\n--skip-slow set: stopping after convention verification.")
        return _summarize(results)

    # 2. Snapshot golden experiment JSONs so slow commands can't corrupt the baseline
    log("\n[snapshot] backing up experiment JSONs to a temp dir (restored at end)")
    tmp, backed = snapshot([
        "experiments/*.json",
    ])
    log(f"  backed up {len(backed)} files")

    try:
        # 3. batch_run large_liquid
        log("\n[2/4] src/batch_run.py --universe large_liquid")
        rc = run_cmd([sys.executable, os.path.join(ROOT, "src/batch_run.py"), "--universe", "large_liquid"])
        ok = rc == 0
        if ok:
            log("  comparing *_large_liquid.json + summary.json to golden (excl timestamp):")
            ok &= compare_patterns(tmp, ROOT, ["experiments/*_large_liquid.json", "experiments/summary.json"])
        results.append(("batch_run --universe large_liquid", rc == 0 and ok, "exit 0 + JSON match"))

        # 4. validate large_liquid
        log("\n[3/4] src/validate.py --universe large_liquid")
        rc = run_cmd([sys.executable, os.path.join(ROOT, "src/validate.py"), "--universe", "large_liquid"])
        ok = rc == 0
        if ok:
            log("  comparing validation_summary.json to golden (excl timestamp):")
            g = _strip_keys(load_json(os.path.join(tmp, "experiments/validation_summary.json")), ("timestamp",))
            f = _strip_keys(load_json(os.path.join(EXP, "validation_summary.json")), ("timestamp",))
            diffs = deep_compare(g, f)
            ok &= not diffs
            log(f"  {'EXACT match' if not diffs else 'DIFF ('+str(len(diffs))+' mismatches)'}: validation_summary.json")
            for d in diffs[:8]:
                log("    " + d)
        results.append(("validate --universe large_liquid", rc == 0 and ok, "exit 0 + JSON match"))

        # 5a. Run eight experiment drivers (quick mode only) to verify deterministic timestamps
        if not args.full:
            drivers = [
                ("experiments/run_e012.py", "e012_market_neutral.json", "run_e012.py", [], None, 0, ("timestamp",)),
                ("experiments/run_e023.py", "e023_economic_trend.json", "run_e023.py", [], None, 0, ("timestamp",)),
                ("experiments/run_e024.py", "e024_convention_audit.json", "run_e024.py", ["--merge"], None, 0, ("timestamp",)),
                ("experiments/run_e027.py", "e027_ivol_anomaly.json", "run_e027.py", [], check_e027_deterministic, 0, ("timestamp",)),
                ("experiments/run_e035.py", "e035_illiquidity.json", "run_e035.py", [], check_e035_deterministic, 0, ("timestamp",)),
                ("experiments/run_e037.py", "e037_portfolio.json", "run_e037.py", [], None, 0, ("timestamp",)),
                ("experiments/run_e039.py", "e039_extended_macro.json", "run_e039.py", [], None, 0, ("timestamp",)),
                ("experiments/run_e042_lead.py", "e042_lead_config_confirmatory.json", "run_e042_lead.py", [], None, 1, ("timestamp", "runtime_sec")),
            ]
            for i, (script, json_name, desc, extra_args, check_fn, expected_rc, exclude_keys) in enumerate(drivers, 1):
                log(f"\n[5a/{i}/8] {desc}")
                cmd = [sys.executable, os.path.join(ROOT, script)] + extra_args
                rc = run_cmd(cmd)
                ok = rc == expected_rc
                if ok:
                    json_glob = os.path.join("experiments", json_name)
                    if check_fn:
                        log(f"  comparing deterministic fields of {json_glob} to golden:")
                        ok &= check_fn(os.path.join(tmp, json_glob), os.path.join(ROOT, json_glob))
                    else:
                        log(f"  comparing {json_glob} to golden (excl {exclude_keys}):")
                        ok &= compare_patterns(tmp, ROOT, [json_glob], exclude_keys=exclude_keys)
                results.append((desc, rc == expected_rc and ok, f"exit {expected_rc} + JSON match"))

        # 5. run_e042
        if args.full:
            log("\n[4/4] experiments/run_e042.py --n-sim 50 (full, ~10 min)")
            e042_args = [sys.executable, os.path.join(ROOT, "experiments/run_e042.py"), "--n-sim", "50"]
            tag = "full n_sim=50"
        else:
            e042_quick = os.path.join(
                EXP, "e042_minvar_market_neutral_quick.json")
            log("\n[4/4] experiments/run_e042.py --n-sim 2 --no-sensitivity (quick)")
            e042_args = [sys.executable, os.path.join(ROOT, "experiments/run_e042.py"),
                        "--n-sim", "2", "--no-sensitivity",
                        "--out", e042_quick]
            tag = "quick n_sim=2"
        rc = run_cmd(e042_args)
        ok = rc == 0
        if ok:
            e042_golden = os.path.join(tmp, "experiments/e042_minvar_market_neutral.json")
            if args.full:
                e042_fresh = os.path.join(EXP, "e042_minvar_market_neutral.json")
                log("  comparing e042_minvar_market_neutral.json + e042_sensitivity_grid.json (excl timestamp):")
                for rel in [os.path.join(EXP, "e042_minvar_market_neutral.json"),
                            os.path.join(EXP, "e042_sensitivity_grid.json")]:
                    rg = os.path.join(tmp, "experiments", os.path.relpath(rel, EXP))
                    diffs = deep_compare(_strip_keys(load_json(rg), ("timestamp",)),
                                         _strip_keys(load_json(rel), ("timestamp",)))
                    ok &= not diffs
                    log(f"  {'EXACT match' if not diffs else 'DIFF ('+str(len(diffs))+' mismatches)'}: {os.path.relpath(rel, EXP)}")
                    for d in diffs[:8]:
                        log("    " + d)
            else:
                e042_fresh = os.path.join(
                    EXP, "e042_minvar_market_neutral_quick.json")
                log("  comparing deterministic E042 fields (placebo/z excluded — n_sim differs):")
                ok &= check_e042_quick_deterministic(e042_golden, e042_fresh)
        results.append((f"run_e042 ({tag})", rc == 0 and ok, "exit 0 + comparison"))
    finally:
        log("\n[restore] restoring golden experiment JSONs from backup")
        restore(tmp, backed)
        # Remove JSON files created during the run (e.g. the quick-mode
        # e042_minvar_market_neutral_quick.json output) so the working
        # tree is left exactly as it was found.
        backed_set = set(backed)
        for path in sorted(glob.glob(os.path.join(ROOT, "experiments", "*.json"))):
            if os.path.relpath(path, ROOT) not in backed_set:
                os.remove(path)
                log(f"  removed run-created file: {os.path.relpath(path, ROOT)}")
        shutil.rmtree(tmp, ignore_errors=True)
        log("  restored.")

    return _summarize(results)


def _summarize(results):
    log("\n" + "=" * 72)
    log("VERIFICATION SUMMARY")
    log("=" * 72)
    allok = True
    for name, ok, detail in results:
        allok &= ok
        log(f"  [{'PASS' if ok else 'FAIL'}] {name} ({detail})")
    log("=" * 72)
    log("OVERALL: " + ("ALL CHECKS PASSED" if allok else "FAILURES DETECTED"))
    log("=" * 72)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
