# Agentic Session Handoff

**Created:** 2026-11-10T07:20:11Z
**Session:** `ses_e3babe2e5ffeeo4kxUzGQYIuKF` (main/code)
**Working tree:** clean (no uncommitted changes)
**HEAD:** `e112d2e6 chore(kilo): checkpoint agent session`

## Task this session
Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.
This file (`HANDOFF.md`) is that durable handoff. No other code changes were made.

## Repo state / context
- Quantitative-strategy research repo (2014–2026 US equities, futures, macro).
- `experiments/*.json` are the canonical research artifacts (committed goldens).
- `AGENTS.md` governs conventions: pre-registration, seed `SEED=42`, verification suite,
  golden integrity, offline data cache, no committing verification output.
- Research phase complete (E001–E043); ledger at `ledger/RESEARCH_LEDGER.md`.
- Closed items: E049/E050 (optimizer determinism) and E041/E042 residual ill-conditioned QP drift
  (~1e-05, 1-ulp sensitivity). Do not re-pin E041/E042 artifacts to silence drift.
- Known data note: `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be
  missing from a fresh working tree (gitignored); a driver needing it may re-download.

## Initial task for the next session
Default action: wait for explicit user instructions. Do not invent experiments, run verification
unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without
explicit direction.

If the user requests work, verify state first:
1. `git status --short --branch` — confirm clean source and note `HEAD` vs `origin/main`.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted:
   `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per
   `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

If asked to run verification, use standard commands with `SEED=42`; **never commit verification
output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report a
golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

## Reproduction / Verification Commands (only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Board
The shared board is empty (no pending peer messages). Use `board_read`/`board_post` only for
material cross-session coordination, not personal bookkeeping.