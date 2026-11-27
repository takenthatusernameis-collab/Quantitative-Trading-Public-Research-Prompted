# Agentic Work Session Handoff — Initial Task

**Timestamp (UTC)**: 2026-11-27T06:51:20Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD**: `main` — `ef16978b23d9535e6c6303903d85763e17d2cfd9` (== `origin/main`)
**Working Tree**: clean for canonical artifacts (`experiments/`, `data/`, `ledger/`); only `__pycache__/*.pyc` (generated) show as modified.

## CLEAR INITIAL TASK (for the next agentic work session)

**Await explicit user instructions before any research action.** Start from a
verified-clean baseline, confirm it, then stop. Do **not** manufacture further
handoff refreshes, re-run the full suite unprompted, or re-pin artifacts unless a
deliberate code change is requested and recorded in the ledger first.

1. **Confirm no active verification run** — `.verify_snapshot/` must NOT exist.
   If a live `ACTIVE.json` owner exists, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete it.
2. **Provision environment** — `pip install -r requirements.txt`.
   `pandas` is NOT installed in this environment; the full suite needs it.
3. **Confirm goldens match HEAD** — `SEED=42 python3 scripts/check_goldens_clean.py`.
4. **Confirm goldens match pinned baseline** —
   `SEED=42 python3 scripts/check_golden_baseline.py` (all pinned artifacts unchanged).
5. **Confirm data coverage** —
   `SEED=42 python3 scripts/check_data_coverage.py` (all pinned inputs present/tracked/unchanged).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).

No code changes are requested yet. The goal of this handoff is to hand the next
session a verified-clean starting point.

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are
documented in `ledger/RESEARCH_LEDGER.md`. Golden artifacts in
`experiments/*.json` are the authoritative record; never re-pin or overwrite
them as a side effect of running verification.

## Git State (2026-11-27T06:51:20Z)

- Branch: `main`; HEAD `ef16978b` == `origin/main` (`ef16978b23d9535e6c6303903d85763e17d2cfd9`).
- Working tree clean except `__pycache__/*.pyc` (generated, not canonical).
- `.verify_snapshot/` absent (no live run owns the snapshot); `.verify_reports/` absent.

## Baseline Integrity (2026-11-27T06:51:20Z)

- ✅ No active verification run: `.verify_snapshot/` does not exist.
- ⚠️ Missing dependency: `pandas` is not installed. Run
  `pip install -r requirements.txt` before the full verification suite.
- Baseline not re-run this session (deps not yet confirmed provisioned).

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050). E041/E042 ill-conditioned-QP drift is closed — artifacts reproduce 0 diffs; do not re-pin to silence a tolerance violation (none remains).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Offline mode: `QUANT_RESEARCH_OFFLINE=1` enforced during verification; an unpinned input fails hard.

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md`
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Handoff Provenance

Supersedes `HANDOFF_2026-11-27T06-44-32Z_INITIAL_TASK.md` (and all earlier
INITIAL_TASK handoffs). This file is the authoritative initial-task message for
the next session. Created at the start of a new agentic work session; no snapshot
recovery needed, no code changes made. The only environment gap is the missing
`pandas` dependency.
