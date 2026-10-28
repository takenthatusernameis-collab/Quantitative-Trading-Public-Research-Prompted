# HANDOFF_NEXT_SESSION_2026-10-28T00-38-11Z

## Initial Task (clear)
Establish a clean, known-good baseline state before any new work. Run the read-only guards first; do not re-run the full verification suite to "refresh" goldens, and do not overwrite `experiments/*.json`.

```bash
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
SEED=42 bash scripts/check.sh
```

If `check_goldens_clean.py` reports a *live* verification, leave it alone. If it reports a stale snapshot or golden mismatch vs HEAD, restore first: `SEED=42 python3 run_all_verification.py --restore-only`. If any guard fails for a reason other than a live run, stop and report before proceeding.

## Context
- Branch: `main`, HEAD: `ed02c9e955d5e4d13de73bf4be600149eefc5d18`
- Working tree: clean of tracked changes (only `__pycache__/*.pyc` artifacts possible).
- No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). Nothing to recover.
- Research phase complete (E001–E043); surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical goldens; verification restores them. Never re-pin to silence drift.
- Known drift: E041 (~133 numeric diffs, ill-conditioned QP), E030 (~28 numeric diffs) — reporting-only, decisions unchanged, do not re-pin.

## Guardrails
- Use `SEED=42` everywhere.
- Never commit verification output or overwrite goldens as a side effect.
- Never re-pin goldens to silence known numeric drift.
- Never add unpinned data downloads; commit cache files and update pins only with explicit rationale.
- Offline safety: verification uses `QUANT_RESEARCH_OFFLINE=1`.

## Quick Reference
- Fast check: `SEED=42 bash scripts/check.sh`
- Quick verify (8 drivers): `SEED=42 python3 run_all_verification.py`
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Timestamp
Created: 2026-10-28T00:38:11Z (UTC)
