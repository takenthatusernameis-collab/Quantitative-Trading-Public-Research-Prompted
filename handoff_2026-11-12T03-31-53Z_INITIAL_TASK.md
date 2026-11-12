# Agentic Handoff — initial task message

**Created:** 2026-11-12T03:31:53Z
**Session:** next agentic work session
**HEAD:** `76a462f6f8007417d1ce54d355c997eb64bbf6ae` (2026-11-12 03:30:22 +0000) "chore(kilo): checkpoint agent session" on `main`, tracking `origin/main` (in sync, `+0 -0`).

## Immediate task

Resume or continue work on the quantitative-strategy research repo. Before touching anything, run the convention check to confirm the working tree is clean:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

This session verified: `=== All checks passed ===` (exit 0) — 107 pinned golden artifacts match `ledger/golden_baseline.json`, 35 pinned data inputs present/tracked/unchanged, 44 guard/report unit tests, 35 experiment driver import/call-site checks, E024 convention-decomposition gate, E042 min-variance gate. `git status --short --branch` shows only 12 pre-existing `__pycache__/*.pyc` build artifacts (timestamp drift, not committed). `git diff --stat HEAD -- experiments/` → empty. `.verify_snapshot/` absent → no interrupted verification run to recover. `git ls-files experiments/` → 138 tracked entries (107 golden JSONs + 31 drivers).

## Critical baseline-integrity rules (from AGENTS.md)

- `experiments/*.json` are canonical committed goldens; the verification suite overwrites them while running drivers and restores them afterwards. **Never leave a verification run half-finished.**
- If `scripts/check.sh` reports a golden mismatch, fix it **before** committing — a checkpoint commit that captures verification output silently replaces the canonical baseline.
- Never re-pin artifacts as a side effect of running the verification suite — the committed golden is the authoritative record. Re-pinning is deliberate and must use `python3 scripts/check_golden_baseline.py --update` so the replacement is visible in the diff.
- If a run is interrupted, restore before committing:
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  # or
  git checkout -- experiments/
  ```
- `make check`, `make verify`, `make verify-full` provide local equivalents of `scripts/check.sh` / `run_all_verification.py`.

## Common commands

```bash
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # extended (~21 min)
SEED=42 python3 run_all_verification.py --full       # full (~15 min)
SEED=42 python3 run_all_verification.py --skip-slow  # convention only
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # convention only
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50   # min-var confirmatory
SEED=42 QUANT_RESEARCH_OFFLINE=1 python3 experiments/run_e030.py
```

## Research state

Research phase is CLOSED (E001–E043 complete; E044–E165 are documentation/conformance/durable-handoff refreshes only). Last research entry is **E051** (Post-Closure Conformance Pass). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. No OPEN/PENDING/BLOCKED/TODO markers in the ledger.

## Known open items

- **E041 still drifts 133 numeric diffs** (1-ulp QP sensitivity, ledger E049/E050) — do **not** re-pin to silence. The exact KKT enumeration fix (E050) closed E041/E042 grid artifacts to 0 diffs; the residual is the ill-conditioned tangency QP itself, not the branch selection.
- **E042 min-var confirmatory is PARTIAL** — G2 placebo z fails (z ~1.7–1.8 vs bar 3.0); not promoted. Its `/primary` block reproduces to 5e-9.
- The CI gate (`.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md`) is complete and accurate; a human maintainer must copy it into `.github/workflows/verification-gate.yml` via the GitHub UI. Do not write under `.github/workflows/` (controller restores that directory; repo token lacks `workflows` push permission).

## Conventions

- Always use `SEED=42`.
- Run `python3 -m py_compile` on changed Python files (no separate linter configured).
- Do not commit verification output or secrets/keys.
- The `__pycache__/*.pyc` noise in the working tree is gitignored and ignored by all guards.