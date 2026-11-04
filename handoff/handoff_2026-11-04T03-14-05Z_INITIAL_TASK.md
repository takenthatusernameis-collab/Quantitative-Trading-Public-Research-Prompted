# INITIAL TASK - Handoff for Next Agent Session

# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T03-14-05Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 0520d91097289405223ef5bd4e5d452055903fc2 (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** pycache modifications only; 0 substantive tracked changes. HEAD == origin/main. No live verification run; `.verify_snapshot/` absent (no run in progress).

## Session Summary (what happened this session)

- Left a timestamped, durable initial-task handoff for the next agentic work session.
- No experiments modified; verification artifacts remain as committed goldens.
- Repository state verified clean before handoff: `git status` shows only `__pycache__` bytecode drift; `git diff --stat HEAD` is empty for tracked source.
- Research phase complete (E001–E049); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (5902 lines).

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*

The next agentic work session must create its own timestamped durable handoff (following the existing naming pattern `handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` in the root and mirrored under `handoff/`) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism, E041/E042 ill-conditioned QP drift).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended # (~21 min, +18 committed drivers)
SEED=42 python3 run_all_verification.py --full     # (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs, no writes)
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents (see AGENTS.md). Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff_2026-11-04T03-11-30Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root symlink targets updated (handoff_current.md, handoff_next.md, handoff_next_session.md, handoff_next_session_LATEST.md, handoff.md, NEXT_HANDOFF.md, NEXT_SESSION_HANDOFF.md, next_session.md, next_session_handoff.md).

Handoff written by agent at 2026-11-04T03-14-05Z.

(End of file)

**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 0520d91097289405223ef5bd4e5d452055903fc2 (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** pycache modifications only; 0 substantive tracked changes. HEAD == origin/main. No live verification run; `.verify_snapshot/` absent (no run in progress).

## Session Summary (what happened this session)

- Left a timestamped, durable initial-task handoff for the next agentic work session.
- No experiments modified; verification artifacts remain as committed goldens.
- Repository state verified clean before handoff: `git status` shows only `__pycache__` bytecode drift; `git diff --stat HEAD` is empty for tracked source.
- Research phase complete (E001–E049); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (5902 lines).

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !*

The next agentic work session must create its own timestamped durable handoff (following the existing naming pattern `handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` in the root and mirrored under `handoff/`) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism, E041/E042 ill-conditioned QP drift).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended # (~21 min, +18 committed drivers)
SEED=42 python3 run_all_verification.py --full     # (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
SEED=42 python3 verify_convention_robustness.py     # convention robustness only (reads JSONs, no writes)
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents (see AGENTS.md). Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff_2026-11-04T03-11-30Z_INITIAL_TASK.md`). This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root symlink targets updated (handoff_current.md, handoff_next.md, handoff_next_session.md, handoff_next_session_LATEST.md, handoff.md, NEXT_HANDOFF.md, NEXT_SESSION_HANDOFF.md, next_session.md, next_session_handoff.md).

Handoff written by agent at 2026-11-04T03-14-05Z.

(End of file)
