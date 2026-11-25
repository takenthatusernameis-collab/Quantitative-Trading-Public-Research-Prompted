# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-25T07:18:01Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `9d6c3a761843cc57877ffa47ef2af952a6cb249e` (2026-11-25 07:17:52 +0000, "chore(kilo): checkpoint agent session")
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**origin/main == HEAD** (no ahead/behind delta)
**git status --short:** clean (no modifications, untracked files, `.verify_snapshot/`, or `.verify_reports/`)

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"* — a one-time instruction, not a standing mandate.
- Wrote durable initial-task handoff at repo root following the established pattern (`HANDOFF_NEXT_SESSION_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`).
- Verified repository state against live HEAD before writing: HEAD == `9d6c3a76...`, `git status --short` clean; `experiments/`, `data/`, `ledger/` unmodified.
- Did **not** run verification, modify experiments, change baselines, or take any research action. Left uncommitted pending explicit direction.

## CLEAR INITIAL TASK

**Await explicit user instructions before any research action.**

The next agentic work session must:

1. Confirm canonical state: `git log -1 --format="%H %ci"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main == `9d6c3a76...`, confirm no `.verify_snapshot/` exists.
2. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043 core).
3. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
4. If this session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_NEXT_SESSION_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

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

Supersedes the previous INITIAL_TASK handoff (`HANDOFF_2026-11-25T01-27-46Z_INITIAL_TASK.md`, HEAD `9d6c3a76...`). This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-25T07:18:01Z.
(End of file)
