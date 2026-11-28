# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-28T06:37:53Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `285c36a62be6756efa8f9d38823e2b95b32b577a` (2026-11-28 06:37:46 +0000) == origin/main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean of tracked source (only ignored `src/__pycache__/*.pyc` modified). No `.verify_snapshot/`. `experiments/`, `data/`, `ledger/` match HEAD.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Verified live state before writing: HEAD == origin/main == `285c36a62be6756efa8f9d38823e2b95b32b577a`; working tree clean of tracked source; no interrupted verification run pending.
- `.handoff.md` (authoritative pointer) and `.handoff/` generic aliases repointed to this file via `scripts/repoint_handoff.py`. No canonical artifact, golden, or baseline was modified, re-pinned, or committed. No verification suite was run. No new research performed.

## CLEAR INITIAL TASK

**Await explicit user instructions; do not modify canonical artifacts unprompted.**

The next agentic work session must:

1. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main, confirm no `.verify_snapshot/`.
2. Run `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` to confirm goldens match the pinned baseline (`ledger/golden_baseline.json`).
3. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043).
4. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
5. If this session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root) and refresh `.handoff.md` + repoint `.handoff/` aliases via `scripts/repoint_handoff.py`.

Do **not** re-run the full verification suite, modify `experiments/`, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

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

Supersedes previous durable handoff `.handoff.md` (2026-11-28T06:36:20Z, stale HEAD `4a8dedeb`). This file is the authoritative initial-task message for the next session. Created at the user's explicit request; leads with verified clean state so the next session proceeds to real work instead of rewriting the handoff.

*This handoff was created for the next agentic work session.*
