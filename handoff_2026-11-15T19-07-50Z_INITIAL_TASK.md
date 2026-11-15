# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T19:07:50Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state (verified)
- `git status --short` shows only untracked `__pycache__/*.pyc` noise (gitignored build artifacts). No source/data changes staged by me.
- Baseline integrity (per AGENTS.md): `SEED=42 bash scripts/check.sh` should pass (“=== All checks passed ===”). If you see `ModuleNotFoundError`, run `pip3 install --break-system-packages -r requirements.txt` and retry (do not treat as baseline failure).
- Research phase is **complete (E001–E051)**; surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Prior durable handoffs exist (see `handoff_2026-11-15T19-04-40Z_INITIAL_TASK.md` and `.handoff/` history).

## Initial task for the next agent (do first, in order)
1. **Confirm repo baseline**
   - Run: `SEED=42 bash scripts/check.sh`
   - Expect: exit 0 and “=== All checks passed ===”.
2. **If checks fail for a real reason (not missing deps)**
   - Goldens differ from HEAD: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Restore from the pinned commit if HEAD was incorrectly altered (see `ledger/golden_baseline.json`).
   - Active/stale verification snapshot: recover via `--restore-only`, then recheck.
3. **Then proceed only with explicit user direction**
   - Do **not** run verification or modify `experiments/*.json`, `data/`, `src/`, `scripts/`, `tests/` unless the user asks.
   - Do **not** re-pin baselines without explicit instruction and written justification in the diff.
   - Do **not** commit `__pycache__/*.pyc`.

## Quick reference commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended   # extended
SEED=42 python3 run_all_verification.py --full       # full
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes (from AGENTS.md / known items)
- Always use `SEED=42`. Never leave a verification run half-finished (it backs up/restores `experiments/*.json`).
- E029/E030/E041 have known offline/repro notes; see `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` before acting.
- CI gate workflow file is not managed by agents; template at `.github/workflow-templates/verification-gate.yml`.

## Handoff artifact locations (this file)
- Primary (repo root): `handoff_2026-11-15T19-07-50Z_INITIAL_TASK.md`
- Also copy into: `.handoff/`, `.kilo/handoff/`, `HANDOFFS/` (if present) and repoint generic pointers via `python3 scripts/repoint_handoff.py handoff_2026-11-15T19-07-50Z_INITIAL_TASK.md` when available.
