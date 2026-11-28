# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-28T06:35:33Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — c83cdf81147a9c1bfd0d012136d78d62340c3108 (2026-11-28)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean apart from `src/__pycache__/cache_keys.cpython-312.pyc` (compiled artifact). No `.verify_snapshot/` present. Canonical `experiments/`, `data/`, `ledger/` match HEAD.

## CLEAR INITIAL TASK

**Await explicit user instructions.** No open research task. Research phase closed (E001–E043); surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

The next agentic work session must:

1. Confirm state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main, confirm no `.verify_snapshot/`.
2. Run `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` to confirm goldens match pinned baseline.
3. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items.
4. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
5. Do the user's task, or stop. Do not invent scope.
6. If the session itself hands off, create its own timestamped durable handoff following the established pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

Do **not** re-run verification, modify experiments, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `HANDOFF_2026-11-27T10-46-45Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-28T06:35:33Z.
