# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-24T12:12:03Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `062ec15205e877ccec5eab5a91cd2c7da03e4aa8` (2026-11-24 12:11:56 +0000)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"* — a one-time instruction, not a standing mandate.
- Wrote durable initial-task handoff at repo root following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`), superseding `HANDOFF_2026-11-24T12-07-09Z_INITIAL_TASK.md` (commit `227cda6e`).
- Verified repository state against live HEAD before writing: HEAD == `062ec152`; `git status --short --untracked-files=all` shows only `M src/__pycache__/cache_keys.cpython-312.pyc` (non-canonical bytecode, not a tracked source change); no `.verify_snapshot/` (no interrupted run to recover); `experiments/`, `data/`, `ledger/` unmodified.
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request. Left uncommitted pending explicit direction.

## CLEAR INITIAL TASK

**Await explicit user instructions before any research action.**

The next agentic work session must:

1. Confirm canonical state: `git log -1 --format="%H %ci"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main, confirm no `.verify_snapshot/` exists.
2. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043 core; handoff refreshes tracked separately).
3. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
4. If this session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

Do **not** re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

- `git log -1 --format="%H %ci"` and `git status --short experiments/ data/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists (no interrupted run to recover). If one exists: `SEED=42 python3 run_all_verification.py --restore-only`.
- Read `ledger/RESEARCH_LEDGER.md` for the surviving validated strategies and open items.
- Quick check before any change: `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention. Offline reproducibility enforced via `QUANT_RESEARCH_OFFLINE=1` in the verification suite.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.
- Never commit secrets/keys.

## Handoff provenance

Supersedes the previous INITIAL_TASK handoff (`HANDOFF_2026-11-24T12-07-09Z_INITIAL_TASK.md`, HEAD `062ec152`). This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-24T12:12:03Z.