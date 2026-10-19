#!/usr/bin/env python3
"""Field-level diff between a committed golden artifact and a fresh run.

Purpose: when a verification driver re-executes and its output no longer
matches the committed golden, the suite reports only "MISMATCH". This tool
answers the question the suite cannot: *which* fields changed, and is the
change structural (a key, a list length, a string, a boolean -- never
relaxed) or numeric (floating-point / vintage drift, relaxable up to a
declared relative tolerance)?

The classification mirrors the comparison semantics used by
``run_all_verification.compare_patterns_float`` so that a PASS/FAIL verdict
here means the same thing as in the suite:

  * structural differences (key added/removed, list length change, type
    change, non-numeric value change) ALWAYS fail,
  * numeric differences fail only when the relative delta exceeds --tol.

Usage:
    python3 scripts/diff_golden.py --golden experiments/e030_multiasset_tsm.json \
        --fresh /tmp/fresh.json --tol 1e-4
    python3 scripts/diff_golden.py --golden a.json --fresh b.json --json report.json

Exit codes: 0 = no structural difference and no numeric drift beyond --tol,
1 = drift beyond tolerance or a structural difference, 2 = usage/IO error.
"""
import argparse
import json
import math
import sys
from pathlib import Path

STRUCTURAL_KINDS = (
    "key_added",
    "key_removed",
    "list_length",
    "type_change",
    "value_changed",
)


def _rel_delta(golden, fresh):
    """Relative difference of two numbers, or None when undefined."""
    if golden is None or fresh is None:
        return None
    try:
        g = float(golden)
        f = float(fresh)
    except (TypeError, ValueError):
        return None
    if math.isnan(g) and math.isnan(f):
        return 0.0
    if g == f:
        return 0.0
    if math.isnan(g) or math.isnan(f):
        return float("inf")
    scale = max(abs(g), abs(f))
    if scale == 0.0:
        return float("inf")
    return abs(f - g) / scale


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def diff_tree(golden, fresh, path="", tol=1e-4):
    """Walk two JSON structures and return a list of difference records."""
    diffs = []
    if isinstance(golden, dict) and isinstance(fresh, dict):
        for k in sorted(set(golden) | set(fresh)):
            child = f"{path}/{k}"
            if k not in fresh:
                diffs.append({"path": child, "kind": "key_removed",
                              "golden": golden[k], "fresh": None,
                              "rel_delta": None, "beyond_tol": True})
            elif k not in golden:
                diffs.append({"path": child, "kind": "key_added",
                              "golden": None, "fresh": fresh[k],
                              "rel_delta": None, "beyond_tol": True})
            else:
                diffs += diff_tree(golden[k], fresh[k], child, tol)
    elif isinstance(golden, list) and isinstance(fresh, list):
        if len(golden) != len(fresh):
            diffs.append({"path": path, "kind": "list_length",
                          "golden": len(golden), "fresh": len(fresh),
                          "rel_delta": None, "beyond_tol": True})
        for i, (a, b) in enumerate(zip(golden, fresh)):
            diffs += diff_tree(a, b, f"{path}[{i}]", tol)
    elif _is_number(golden) and _is_number(fresh):
        rel = _rel_delta(golden, fresh)
        if rel is None or rel > tol:
            diffs.append({"path": path, "kind": "numeric_drift",
                          "golden": golden, "fresh": fresh,
                          "rel_delta": rel, "beyond_tol": True})
        else:
            diffs.append({"path": path, "kind": "numeric_within_tol",
                          "golden": golden, "fresh": fresh,
                          "rel_delta": rel, "beyond_tol": False})
    elif type(golden) is not type(fresh):
        diffs.append({"path": path, "kind": "type_change",
                      "golden": golden, "fresh": fresh,
                      "rel_delta": None, "beyond_tol": True})
    else:
        if golden != fresh:
            diffs.append({"path": path, "kind": "value_changed",
                          "golden": golden, "fresh": fresh,
                          "rel_delta": None, "beyond_tol": True})
    return diffs


def _section(path):
    """Top-level section a diff path belongs to."""
    parts = path.split("/")
    return parts[1] if len(parts) > 1 else "(root)"


def _fmt_value(v):
    s = repr(v)
    return s if len(s) <= 80 else s[:77] + "..."


def report(diffs, tol, golden_name, fresh_name, stream=sys.stdout):
    """Print a human-readable diff report; return the failure count."""
    failing = [d for d in diffs if d["beyond_tol"]]
    structural = [d for d in failing if d["kind"] in STRUCTURAL_KINDS]
    numeric = [d for d in failing if d["kind"] == "numeric_drift"]
    within = [d for d in diffs if not d["beyond_tol"]]

    print(f"golden: {golden_name}")
    print(f"fresh : {fresh_name}")
    print(f"tolerance: rel_tol={tol:g}")
    print(f"differences: {len(diffs)} total "
          f"({len(failing)} beyond tolerance, {len(within)} within tolerance)")
    if structural:
        print(f"  STRUCTURAL (never relaxed): {len(structural)}")
    if numeric:
        print(f"  NUMERIC beyond tolerance: {len(numeric)}")
    if within:
        worst = max(within, key=lambda d: d["rel_delta"] or 0.0)
        print(f"  numeric within tolerance: {len(within)} "
              f"(worst rel_delta={worst['rel_delta']:.3e} at {worst['path']})")

    sections = {}
    for d in diffs:
        sections.setdefault(_section(d["path"]), []).append(d)

    for sec in sorted(sections):
        rows = sections[sec]
        bad = [d for d in rows if d["beyond_tol"]]
        max_rel = max((d["rel_delta"] or 0.0) for d in rows)
        head = f"[{sec}] {len(rows)} diff(s), {len(bad)} beyond tolerance"
        if max_rel:
            head += f", max rel_delta={max_rel:.3e}"
        print(f"\n{head}")
        for d in rows:
            flag = "FAIL" if d["beyond_tol"] else "ok  "
            rel = "" if d["rel_delta"] is None else f" rel={d['rel_delta']:.3e}"
            print(f"  {flag} {d['kind']:<18} {d['path']}")
            print(f"       golden={_fmt_value(d['golden'])}")
            print(f"       fresh ={_fmt_value(d['fresh'])}{rel}")

    return len(failing)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--golden", required=True, help="committed golden JSON")
    ap.add_argument("--fresh", required=True, help="freshly produced JSON")
    ap.add_argument("--tol", type=float, default=1e-4,
                    help="relative tolerance for numeric drift (default 1e-4)")
    ap.add_argument("--json", dest="json_out",
                    help="write the full diff record list to this path")
    ap.add_argument("--quiet", action="store_true",
                    help="print only the summary verdict")
    args = ap.parse_args(argv)

    try:
        golden = json.loads(Path(args.golden).read_text())
        fresh = json.loads(Path(args.fresh).read_text())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    diffs = diff_tree(golden, fresh, tol=args.tol)

    if args.quiet:
        failing = [d for d in diffs if d["beyond_tol"]]
        structural = [d for d in failing if d["kind"] in STRUCTURAL_KINDS]
        print(f"{len(diffs)} diff(s); {len(failing)} beyond tol={args.tol:g}; "
              f"{len(structural)} structural")
    else:
        n_fail = report(diffs, args.tol, args.golden, args.fresh)
    failing = [d for d in diffs if d["beyond_tol"]]
    structural = [d for d in failing if d["kind"] in STRUCTURAL_KINDS]

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(diffs, indent=1, default=str))

    if structural:
        print(f"\nVERDICT: FAIL - {len(structural)} structural difference(s)")
        return 1
    if failing:
        print(f"\nVERDICT: FAIL - {len(failing)} numeric difference(s) beyond "
              f"rel_tol={args.tol:g}")
        return 1
    print(f"\nVERDICT: PASS - no structural difference, no numeric drift beyond "
          f"rel_tol={args.tol:g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
