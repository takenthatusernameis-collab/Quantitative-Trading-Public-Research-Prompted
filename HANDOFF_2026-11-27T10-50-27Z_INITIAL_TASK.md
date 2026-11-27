# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-27T10:50:27Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — b2c1374915b3846cea1957acfa79b904a602b0de (2026-11-27 10:49:59 +0000) == origin/main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** `.verify_snapshot/` PRESENT with `ACTIVE.json` (pid 124131) — that process is DEAD. Interrupted verification run pending recovery. Canonical `experiments/`, `data/`, `ledger/` currently match HEAD (`git status --short` clean for those paths).

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Wrote this durable initial-task handoff at repo root, superseding the prior INITIAL_TASK handoff (`HANDOFF_2026-11-27T10-46-45Z_INITIAL_TASK.md`).
- Verified live state before writing: HEAD == `b2c1374915b3846cea1957acfa79b904a602b0de` == origin/main; `.verify_snapshot/ACTIVE.json` present but owning pid 124131 is dead; `git status --short experiments/ data/ ledger/` clean; core deps import OK (numpy 2.5.4, pandas, scipy, pyarrow, statsmodels).

## CLEAR INITIAL TASK

**Recover the interrupted verification run first, then await explicit user instructions.**

The next agentic work session must:

1. Recover the interrupted verification run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Confirm `.verify_snapshot/` is removed afterward.
2. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main, confirm no `.verify_snapshot/`.
3. Run `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` to confirm goldens match the pinned baseline (`ledger/golden_baseline.json`).
4. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043).
5. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
6. If this session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root) and update the durable pointer (`.handoff.md`).

Do **not** re-run the full verification suite, modify `experiments/`, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

- Recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
- `git log -1 --format="%H"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists (no interrupted run left to recover).
- Read `ledger/RESEARCH_LEDGER.md` for the surviving validated strategies and open items.
- Quick check before any change: `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoff `HANDOFF_2026-11-27T10-46-45Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-27T10:50:27Z.