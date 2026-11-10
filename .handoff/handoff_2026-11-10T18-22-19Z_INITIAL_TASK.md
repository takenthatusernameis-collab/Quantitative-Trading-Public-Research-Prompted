# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T18:22:19Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `d7a5f332` (`chore(kilo): checkpoint agent session`) — `origin/main` in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Verified State

- `git status --short --branch`: `## main...origin/main`; only ` M src/__pycache__/cache_keys.cpython-312.pyc` (untracked bytecode artifact; do not commit unless explicitly instructed).
- `.verify_snapshot/`: **absent** (no interrupted verification run).
- Research phase **complete (E001–E043)**; authoritative dispositions: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines authoritative: `experiments/*.json` + `ledger/golden_baseline.json` + `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of verification.
- Baseline guards (re-run this session): `scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**; `scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**.
- Tracked golden artifacts: 138 `experiments/*.json` files, all matching HEAD.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration). E041/E042 residual 1-ulp/ill-conditioned QP drift (29–133 numeric diffs) remains expected; **never re-pin** E041/E042 artifacts to silence it.
- `data/panel.parquet` is pinned in `ledger/data_baseline.json` but gitignored; verification runs with `QUANT_RESEARCH_OFFLINE=1` so a missing pinned cache fails hard.

## Initial Task for Next Session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or alter golden/data baselines without explicit direction.

**If asked to work:**
1. `git status --short --branch` — confirm clean source and HEAD vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`).

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report mismatch, restore/fix — do not re-pin to silence.

## Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails

- **SEED=42** for reproducibility/verification.
- Never commit driver output over canonical goldens; never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use template/maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys or stage `__pycache__/*.pyc`.

## Provenance

- **This handoff:** `handoff_2026-11-10T18-22-19Z_INITIAL_TASK.md`
- **Previous:** `handoff_2026-11-10T18-21-13Z_INITIAL_TASK.md`
