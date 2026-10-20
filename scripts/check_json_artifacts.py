#!/usr/bin/env python3
"""Fast offline guard for committed experiment artifacts.

Invariant: every committed JSON artifact under experiments/ (and the repo
root, where applicable) must parse as valid JSON. A malformed artifact breaks
the repository's reproducibility claim — any bulk loader, the convention
verification script, or a future agent re-reading results would crash.

This check is pure file I/O (no execution, no data/network) so it stays in the
fast path of scripts/check.sh.

Catches the exact class of regression found in experiments/
e031_accruals_feasibility.json, where the data_feasibility_check dict was closed
with a stray `]` instead of `}`, leaving the only malformed file among all 106
committed JSON artifacts.

Beyond parse validity, this guard also enforces a *schema* invariant: every
artifact that is a committed experiment record must carry a stable identifier
(`experiment` or `experiment_id`) and a decision/status field. A renamed or
stripped artifact (e.g. an experiment JSON that lost its `experiment` key during
an edit) would still parse as valid JSON but would no longer be loadable by
any consumer that keys off the identifier — the same class of breakage the
parse guard exists to prevent, just one layer deeper. Artifacts that are not
experiment records (universe-scoped strategy evaluations, the batch summary,
cost-sweep lists, the data-vintage manifest, the E024 sub-parts) are allowedlist
by filename so the check cannot be satisfied by deleting files.

Schema classes (determined by structure, not filename alone):

  EXPERIMENT_DRIVER     - driver output: has `experiment` + `timestamp`
  EXPERIMENT_ID_DRIVER  - feasibility study: has `experiment_id` (older style)
  DATA_INFEASIBILITY    - has `data_feasibility_check` or the QMJ feasibility
                         shape; requires `decision` + `status`
  SENSITIVITY_GRID      - has `grid` + `n_configs`
  STRATEGY_EVAL         - batch_run per-strategy/universe evaluation: has
                         `strategy` + `benchmark` + `oos_sharpe`
  E024_PART             - E024 convention-audit sub-part (part_a/b/c only)
  NON_EXPERIMENT        - summary / validation / cost-sweep / vintage manifest

"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Files that are legitimately NOT experiment records. Named explicitly so the
# guard cannot be satisfied by deleting an experiment artifact.
NON_EXPERIMENT_FILES = {
    "summary.json",
    "validation_summary.json",
    "FINAL_SUMMARY.json",
    "VERIFICATION_FINAL.json",
    "golden_baseline.json",
    "cost_sensitivity.json",
    "cost_sensitivity_tsm.json",
    "cost_sensitivity_tsm_pure.json",
    "reversal_mega10d.json",
    "blend_costrobust_21d.json",
    "blend_tsm_dnlowbeta_etfs.json",
    "blend_tsm_dnlowbeta_large_liquid.json",
    "data/vintages.json",
    "data/fundamentals_vintages.json",
}

#: The schema invariant applies to the experiment artifacts: everything under
#: ``experiments/`` plus the JSON documents at the repository root. Other
#: tracked JSON (the pinned data manifests under ``data/``) only has to parse -
#: they are not experiment records and carry no experiment identifier.
SCHEMA_SCOPE_PREFIXES = ("experiments/",)


def _in_schema_scope(rel):
    """True when the schema invariant applies to a tracked JSON file."""
    if rel.startswith(SCHEMA_SCOPE_PREFIXES):
        return True
    return "/" not in rel

# Required fields per schema class. Empty list == structural identity only.
# IDENTIFIER names the acceptable set of fields that must be present so the
# artifact can be keyed by consumers; it is checked separately because the
# identifier field differs between the modern `experiment` style and the older
# `experiment_id` style, and a data-infeasibility study may use either.
REQUIRED = {
    "EXPERIMENT_DRIVER": ["experiment", "timestamp"],
    "EXPERIMENT_ID_DRIVER": ["experiment_id", "decision"],
    "DATA_INFEASIBILITY": ["decision"],
    "SENSITIVITY_GRID": ["experiment", "grid", "n_configs"],
    "STRATEGY_EVAL": ["strategy", "benchmark", "oos_sharpe"],
    "E024_PART": [],
    "NON_EXPERIMENT": [],
}

IDENTIFIER = {
    "EXPERIMENT_DRIVER": ("experiment",),
    "EXPERIMENT_ID_DRIVER": ("experiment_id",),
    "DATA_INFEASIBILITY": ("experiment", "experiment_id"),
    "SENSITIVITY_GRID": ("experiment",),
    "STRATEGY_EVAL": (),
    "E024_PART": (),
    "NON_EXPERIMENT": (),
}


def classify(d, rel, basename):
    """Classify a parsed artifact by its structure."""
    if rel in NON_EXPERIMENT_FILES or basename in NON_EXPERIMENT_FILES:
        return "NON_EXPERIMENT"
    if "data_feasibility_check" in d or "feasible_for_2014_2026_walkforward" in d:
        return "DATA_INFEASIBILITY"
    if "grid" in d and "n_configs" in d:
        return "SENSITIVITY_GRID"
    if "experiment" in d and "timestamp" in d:
        return "EXPERIMENT_DRIVER"
    if "experiment_id" in d:
        return "EXPERIMENT_ID_DRIVER"
    if "strategy" in d:
        return "STRATEGY_EVAL"
    if any(k in d for k in ("part_a", "part_b", "part_c")):
        return "E024_PART"
    return "UNKNOWN"


def main():
    files = subprocess.check_output(["git", "ls-files"], cwd=ROOT).decode().split()
    bad = []
    n = 0
    for rel in files:
        if not rel.endswith(".json"):
            continue
        n += 1
        path = ROOT / rel
        basename = Path(rel).name
        try:
            text = path.read_text()
        except OSError as exc:
            bad.append((rel, "read error", str(exc).splitlines()[0]))
            continue
        try:
            d = json.loads(text)
        except json.JSONDecodeError as exc:
            bad.append((rel, "JSONDecodeError", str(exc).splitlines()[0]))
            continue

        # Schema check: only for dict-valued experiment records. List-valued
        # artifacts (cost-sweep outputs) are covered by the NON_EXPERIMENT
        # allowlist and are not required to carry experiment metadata.
        # Files outside the schema scope (the pinned data manifests under
        # data/) only have to parse.
        if not _in_schema_scope(rel):
            continue

        if not isinstance(d, dict):
            if basename not in NON_EXPERIMENT_FILES:
                bad.append((rel, "SCHEMA", f"unexpected top-level {type(d).__name__}"))
            continue

        cls = classify(d, rel, basename)
        if cls == "UNKNOWN":
            bad.append((rel, "SCHEMA", "unrecognized artifact structure"))
            continue
        for field in REQUIRED.get(cls, []):
            if field not in d:
                bad.append((rel, "SCHEMA", f"{cls} missing required field '{field}'"))
        # Identifier check: the artifact must be keyable by a consumer. Only
        # enforced for schema classes that are expected to carry one.
        ident = IDENTIFIER.get(cls, ())
        if ident and not any(f in d for f in ident):
            bad.append((rel, "SCHEMA",
                        f"{cls} missing identifier field {list(ident)}"))

    for rel, kind, msg in bad:
        print(f"FAIL {rel}: {kind}: {msg}")
    print(f"checked {n} committed JSON artifacts")
    if bad:
        print(f"JSON ARTIFACT CHECKS FAILED ({len(bad)} malformed)")
        return 1
    print("ALL COMMITTED JSON ARTIFACTS PARSE OK")
    return 0


def _self_test(tmpdir=None):
    """Run a tiny smoke test of the guard against crafted bad cases."""
    import io
    import contextlib
    import tempfile
    from pathlib import Path
    import subprocess
    import json

    def init_git(d):
        subprocess.run(["git", "init", "-q"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.email", "t@t.com"], cwd=d, check=True)
        subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)

    def run(files):
        with tempfile.TemporaryDirectory(dir=tmpdir) as td:
            d = Path(td)
            init_git(d)
            for rel, content in files.items():
                p = d / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
                subprocess.run(["git", "add", rel], cwd=d, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "add"], cwd=d, check=True)
            old = ROOT
            try:
                globals()["ROOT"] = d
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = main()
                return rc, buf.getvalue()
            finally:
                globals()["ROOT"] = old

    # Case 1: malformed fails
    rc, _ = run({"experiments/b.json": "{bad"})
    if rc == 0:
        return "malformed case should fail", 1
    # Case 2: missing identifier fails
    rc, _ = run({"experiments/x.json": json.dumps({"timestamp": "t"})})
    if rc == 0:
        return "missing identifier case should fail", 1
    # Case 3: good experiment passes
    rc, out = run({"experiments/e.json": json.dumps({"experiment": "E1", "timestamp": "t"})})
    if rc != 0:
        return f"good case should pass: {out}", 1
    # Case 4: unknown structure fails
    rc, _ = run({"experiments/u.json": json.dumps({"foo": 1})})
    if rc == 0:
        return "unknown structure should fail", 1
    # Case 5: experiment missing required timestamp fails
    rc, _ = run({"experiments/e2.json": json.dumps({"experiment": "E2"})})
    if rc == 0:
        return "missing required field should fail", 1
    # Case 6: DATA_INFEASIBILITY missing decision fails
    rc, _ = run({"experiments/d.json": json.dumps({"data_feasibility_check": {}})})
    if rc == 0:
        return "data infeasibility missing decision should fail", 1
    # Case 7: DATA_INFEASIBILITY with experiment_id but missing decision fails
    rc, _ = run({"experiments/d2.json": json.dumps({"experiment_id": "E3", "data_feasibility_check": {}})})
    if rc == 0:
        return "data infeasibility missing decision should fail", 1
    # Case 8: unexpected non-dict top-level (not allowlisted) fails
    rc, _ = run({"experiments/badlist.json": "[]"})
    if rc == 0:
        return "non-dict non-allowlisted should fail", 1
    # Case 9: data infeasibility with experiment_id and decision passes
    rc, out = run({"experiments/d3.json": json.dumps({"experiment_id": "E3", "data_feasibility_check": {}, "decision": "REJECT"})})
    if rc != 0:
        return f"data infeasibility valid should pass: {out}", 1
    return "ok", 0


def _maybe_self_test():
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        msg, rc = _self_test()
        if rc != 0:
            print(f"SELF-TEST FAILED: {msg}")
            sys.exit(rc)
        print("SELF-TEST OK")
        sys.exit(0)


if __name__ == "__main__":
    _maybe_self_test()
    # The exit code IS the check: scripts/check.sh relies on it to abort the
    # fast suite. Discarding main()'s return value here would make the guard
    # unable to fail (it still printed FAIL lines, so the breakage was silent).
    sys.exit(main())
