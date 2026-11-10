# Durable Handoff — Quantitative Trading Research

**Timestamp:** 2026-11-10T23:38:57Z
**Session:** New session - 2026-11-10T23:38:54.473Z
**Working tree:** clean, no uncommitted changes
**No open blockers.**

## Project state
Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. Canonical research artifacts live in `experiments/*.json` (committed goldens).

## Immediate task for next session
Run the fast convention check from AGENTS.md:
```
SEED=42 bash scripts/check.sh
# or: make check
```
Then optionally fuller verification:
```
SEED=42 python3 run_all_verification.py        # verify-quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Key constraints (read AGENTS.md before running)
- `experiments/*.json` are backed up and restored by `run_all_verification.py`; a run must never be left half-finished.
- Never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- Committed artifacts must match SHA-256 fingerpins in `ledger/golden_baseline.json` (`scripts/check_golden_baseline.py`).
- Offline mode `QUANT_RESEARCH_OFFLINE=1` requires pinned caches (`scripts/check_data_coverage.py`).
- No separate linter; run `python3 -m py_compile` on changed files.

## Pending work
No specific feature/bug task assigned. Await user direction.
