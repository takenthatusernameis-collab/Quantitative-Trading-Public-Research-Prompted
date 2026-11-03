# HANDOFF — 2026-11-03T11:16:53Z

## Current state
- **Repo:** Quantitative-Trading-Public-Research-Prompted (git repo, Linux)
- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Baselines:** Canonical artifacts in `experiments/*.json` pinned by `ledger/golden_baseline.json`. Data coverage pinned by `ledger/data_baseline.json`.
- **Verification discipline:** Suite backs up/restores goldens; snapshot lives in gitignored `.verify_snapshot/` with `ACTIVE.json`. Do **not** leave a verification run half-finished.

## Initial task for next agent
1. **Confirm baseline integrity first.** Run `SEED=42 bash scripts/check.sh`. All steps must pass before making changes.
2. **Read the ledger.** Review `ledger/RESEARCH_LEDGER.md` end-to-end, paying special attention to open items (notably E041 numeric drift / optimizer determinism) and any PARTIAL/REJECTED rationale.
3. **Stabilize if broken.** If `check.sh` reports golden mismatch or stale snapshot, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). If HEAD already replaced baselines, restore the commit whose SHA-256 matches `ledger/golden_baseline.json`.
4. **Investigate drift only with justification.** The extended verification reports bounded numeric drift for some drivers (E041 has remaining 1-ulp sensitivity). **Do not** re-pin goldens to silence verification failures. Any re-pin must be justified by a pre-registered fix and done via `python3 scripts/check_golden_baseline.py --update`.

## Key files to read first
- `AGENTS.md` — project commands, invariants, and verification rules
- `ledger/RESEARCH_LEDGER.md` — decisions, gates, falsifications, open items
- `ledger/golden_baseline.json` / `ledger/data_baseline.json`
- `run_all_verification.py` / `scripts/check.sh`

## Quick commands
```bash
# Baseline integrity
SEED=42 bash scripts/check.sh

# Full verification (full grid + n_sim=50)
SEED=42 python3 run_all_verification.py --full

# Recovery after interrupted run
SEED=42 python3 run_all_verification.py --restore-only

# Guards
python3 scripts/check_goldens_clean.py
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
```

## Critical notes
- **Cache is enforced:** Missing/unpinned data fails under `QUANT_RESEARCH_OFFLINE=1`. Commit inputs and re-pin via `scripts/check_data_coverage.py --update`.
- **E029/E030:** Fundamentals pinned in `data/fundamentals/`; E030 panel committed (offline-reproducible).
- **Optimizer rule:** Validate solver answers on problem constraints, never on solver exit status (status 8 can be acceptable). Tangency remains ill-conditioned → expect bounded numeric drift.
- **Do not commit verification output.** If interrupted, restore goldens before committing.
