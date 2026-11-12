# Agentic Handoff — Initial Task Message

**Created:** 2026-11-12T04:14:57Z (UTC)
**Repo:** `Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `fa58ebdc281155af3005c3cce737e21ee9db98c3` chore(kilo): checkpoint agent session

## Immediate first actions

1. Inspect workspace state: `git status --short` (working tree is clean — no tracked modifications, no `__pycache__` drift in this snapshot).
2. Confirm baseline/invariants before any edits: `SEED=42 bash scripts/check.sh` (or `make check`).
3. If `check.sh` reports golden mismatches under `experiments/`, restore/fix before committing — never commit verification output or leave a verification run half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD holds the true golden).

## Repo context / conventions

- Canonical artifacts: `experiments/*.json` are committed goldens; verification runs overwrite then restore them.
- Reproducibility: always use `SEED=42`. Data inputs/caches are pinned; suite re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for commands, guards, and experiment dispositions.
- No separate linter configured; run `python3 -m py_compile` on changed Python files. Follow existing code style; no comments/emojis unless requested. Do not commit secrets.

## Useful commands

- `SEED=42 bash scripts/check.sh` / `make check` — fast convention/baseline checks
- `SEED=42 python3 run_all_verification.py` — quick verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only
- `SEED=42 python3 src/batch_run.py --universe large_liquid`
- `SEED=42 python3 src/validate.py --universe large_liquid`
- `SEED=42 python3 experiments/run_e042.py --n-sim 50` — min-var confirmatory

## Verified state at handoff

- `git status --short --branch` → `## main...origin/main` (in sync, `+0 -0`); **working tree clean**, no tracked modifications, no `__pycache__/*.pyc` drift.
- `git ls-files experiments/` → 138 tracked entries (107 golden JSONs + 31 drivers).
- `.verify_snapshot/` absent → no interrupted verification run to recover.
- `SEED=42 python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**.
- `SEED=42 python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**.
- `SEED=42 bash scripts/check.sh` → **13 of 15 steps pass** (exit 1 is environmental only): golden-clean guard, golden-baseline guard, data-coverage guard, JSON-artifact guard (114 committed JSONs parse OK), 4 guard/report unit tests, convention-robustness gate, template validation, experiment import/call-site checks all pass. The 2 failing steps (`tests.test_data_coverage`, `tests.test_portfolio_opt`) fail with `ModuleNotFoundError: No module named 'numpy'/'pandas'` — the sandbox `/usr/bin/python3` has none of `requirements.txt` installed; install with `pip install -r requirements.txt` to make `check.sh` exit 0.

## Known open items (do not paper over)

- **E041:** 133 numeric diffs remain from 1-ulp QP sensitivity (ledger E049); extended verification still reports drift. Do **not** re-pin `experiments/e041*.json` to silence this.
- **E042:** min-var confirmatory is **PARTIAL** (4/5; G2 β-constrained placebo z 2.11 < 3.0 FAIL); market-neutral-total-portfolio line is **CLOSED**, not promoted. Confirmatory run with full placebo already executed and recorded — no further promotion path.
- **Process:** never re-pin golden/data baselines as a side effect of verification; baseline replacement requires explicit `--update` + review.
- **CI gate**: `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md` are complete and accurate; a human maintainer must copy the template into `.github/workflows/verification-gate.yml` via the GitHub UI. Do not write under `.github/workflows/` (controller restores that directory; repo token lacks `workflows` push permission).

## Suggested next-session task

- Start with `git status --short` and `SEED=42 bash scripts/check.sh` to establish a clean, verified baseline (expect exit 1 only from missing numpy/pandas — install `pip install -r requirements.txt` to clear it; all 13 other steps pass).
- The repository is closed (E001–E043 complete; E051 last research entry; E052–E166 durable-handoff refreshes only). No actionable OPEN/PENDING/BLOCKED/TODO markers.
- Any new work must be pre-registered with falsification expectations and sensitivity grids before execution; goalposts are never moved post-hoc. Record outcomes honestly in the ledger (REJECTED / PARTIAL with evidence).