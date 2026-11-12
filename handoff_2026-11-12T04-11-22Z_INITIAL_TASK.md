# Agentic Handoff — Initial Task Message

**Created:** 2026-11-12T04:11:22Z (UTC)
**Repo:** `Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `4fa30b62` chore(kilo): checkpoint agent session (research phase complete, E001–E043)

## Immediate first actions

1. Inspect workspace state: `git status --short` (note: `src/__pycache__/cache_keys.cpython-312.pyc` is currently modified in this snapshot; do not commit generated artifacts/pyc).
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

- `git status --short --branch` → `## main...origin/main` (in sync, `+0 -0`); 1 tracked modification only: `src/__pycache__/cache_keys.cpython-312.pyc` (pyc build artifact, timestamp drift, not committed).
- `git ls-files experiments/` → 138 tracked entries (107 golden JSONs + 31 drivers).
- `.verify_snapshot/` absent → no interrupted verification run to recover.
- `SEED=42 python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**.
- `SEED=42 python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**.

## Known open items (do not paper over)

- **E041:** 133 numeric diffs remain from 1-ulp QP sensitivity (ledger E049); extended verification still reports drift. Do **not** re-pin `experiments/e041*.json` to silence this.
- **E042:** min-var confirmatory is **PARTIAL** (4/5; G2 β-constrained placebo z 2.11 < 3.0 FAIL); market-neutral-total-portfolio line is **CLOSED**, not promoted. Confirmatory run with full placebo already executed and recorded — no further promotion path.
- **Process:** never re-pin golden/data baselines as a side effect of verification; baseline replacement requires explicit `--update` + review.

## Suggested next-session task

- Start with `git status --short` and `SEED=42 bash scripts/check.sh` to establish a clean, verified baseline.
- The repository is closed (E001–E043 complete; E051 last research entry; E052–E161 durable-handoff refreshes only). No actionable OPEN/PENDING/BLOCKED/TODO markers.
- Any new work must be pre-registered with falsification expectations and sensitivity grids before execution; goalposts are never moved post-hoc. Record outcomes honestly in the ledger (REJECTED / PARTIAL with evidence).