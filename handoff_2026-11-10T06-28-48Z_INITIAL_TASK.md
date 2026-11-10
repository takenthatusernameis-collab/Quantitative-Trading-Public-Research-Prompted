# Agentic Session Handoff

**Created:** 2026-11-10T07:19:43Z
**Session:** `ses_e3bac54caffeAECSwGNQ1KFQE4` (main/code)
**Working tree:** clean (no uncommitted changes)
**HEAD:** `04cfc975 chore(kilo): checkpoint agent session`

## Task this session
Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.
This file (`HANDOFF.md`) is that durable handoff. No other code changes were made.

## Repo state / context
- Quantitative-strategy research repo (2014–2026 US equities, futures, macro).
- `experiments/*.json` are the canonical research artifacts (committed goldens).
- `AGENTS.md` governs conventions: pre-registration, seed `SEED=42`, verification suite,
  golden integrity, offline data cache, no committing verification output.

## Initial task for the next session
Run the convention-robustness check / verification and confirm the working tree stays clean:

```bash
SEED=42 bash scripts/check.sh
# or: make check
```

If a fuller verification is desired:

```bash
SEED=42 python3 run_all_verification.py --skip-slow
```

**Critical rules (from AGENTS.md):**
- Never leave a verification run half-finished; it overwrites `experiments/*.json` and restores
  afterwards. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Never commit verification output over the canonical baseline; re-pinning goldens requires
  `python3 scripts/check_golden_baseline.py --update` and puts the replacement in the diff.
- Data inputs must be pinned via `python3 scripts/check_data_coverage.py --update` before use;
  the suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`.

## Board
The shared board is empty (no pending peer messages). Use `board_read`/`board_post` only for
material cross-session coordination, not personal bookkeeping.
