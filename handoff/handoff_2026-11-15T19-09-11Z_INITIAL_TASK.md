# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T19-09-11Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state
- Research phase **complete (E001–E051)**. Surviving validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines/artifacts: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned data/fundamentals per `data/vintages.json` and `data/fundamentals_vintages.json`.
- `git status --short`: only untracked `__pycache__/*.pyc` (gitignored) observed at handoff time; no source/data/experiment changes staged by this session.
- Prior durable handoff: `handoff_2026-11-15T19-07-50Z_INITIAL_TASK.md` (superseded by this file).

## Initial task for the next agent (do first)
1. **Confirm baseline integrity**
   - Run: `SEED=42 bash scripts/check.sh`
   - Expect: exit 0 and `=== All checks passed ===`.
   - If deps are missing, run `pip3 install --break-system-packages -r requirements.txt` and retry (not a baseline failure).
2. **If checks fail for a real baseline issue**
   - Dirty goldens/stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `ledger/golden_baseline.json`). Do not commit captured verification output.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
3. **Proceed only with explicit user direction**
   - Default: await instructions. Do **not** run long verification, invent experiments, or change gates/outcomes unprompted.
   - Do **not** modify/re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without explicit request and justified diff.
   - Never leave a verification run half-finished; do not commit `__pycache__`.

## Quick reference
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Handoff artifact
- Primary: `handoff_2026-11-15T19-09-11Z_INITIAL_TASK.md`
- Mirrored/copied to available handoff dirs and generic pointers repointed via `scripts/repoint_handoff.py`.
