# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T03-54-48Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 871d08ea4c74ad5a0be637901a600b6f5d8b6a28 (== origin/main)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean except for this session's handoff artifacts (new `handoff_2026-11-04T03-54-48Z_INITIAL_TASK.md` + `handoff/` mirror, repointed symlinks, and the appended uncommitted ledger entry E081 — matching the E075–E080 pattern of appending during the session and letting the checkpoint commit carry it). `git diff --stat HEAD -- experiments/` empty (138 goldens match HEAD); no source/test change. No live verification run; `.verify_snapshot/` absent (nothing to recover).

## Session Summary (what happened this session)

- Responded to the user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Verified repository state against live HEAD before writing: HEAD == origin/main, tracked tree clean, experiments/ goldens match HEAD, no `.verify_snapshot/`, no untracked non-`__pycache__` files.
- Read the prior standing handoff (`handoff_2026-11-04T03-53-43Z_INITIAL_TASK.md`, HEAD `efd4c9d`) and the ledger tail (E001–E080). The prior handoff is stale vs current HEAD `871d08e`; superseded, not re-adopted.
- Did **not** run verification, modify experiments, change baselines, or commit anything. No research action taken — per the standing instruction to wait for explicit user direction.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` in the root, mirrored under `handoff/`, and repointing all root + `.kilo/handoff/` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

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
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050 — exact KKT enumeration routes the tangency QP; E041/E042 grid artifacts reproduce 0 diffs).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents (see AGENTS.md). Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs (most recent prior: `handoff_2026-11-04T03-53-43Z_INITIAL_TASK.md` at HEAD `efd4c9d`). This file is the authoritative initial-task message for the next session.
Durable copies written to: `handoff/`, root symlink targets updated (handoff_current.md, handoff_next.md, handoff_next_session.md, handoff_next_session_LATEST.md, handoff.md, NEXT_HANDOFF.md, NEXT_SESSION_HANDOFF.md, next_session.md, next_session_handoff.md, HANDOFF.md, HANDOFF_CURRENT.md, HANDOFF_NEXT.md, HANDOFF_NEXT_SESSION.md, HANDOFF_NEXT_SESSION_LATEST.md).

Handoff written by agent at 2026-11-04T03:54:48Z.

(End of file)