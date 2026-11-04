# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T12-53-38Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main (`30e1cbe5232a76dc9e06ec66fd7e54354239bcbf`)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- Research phase complete (E001-E043); surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are committed goldens; do not modify without explicit direction.
- Baseline pins: `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Do not re-pin as a side effect.
- `.verify_snapshot/` absent (no live verification run). Working tree has only tracked `__pycache__/*.pyc` modifications (harmless bytecode, not committed).
- Prior handoff: `handoff/handoff_2026-11-04T12-53-14Z_INITIAL_TASK.md` (superseded).

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Created this timestamped durable handoff following the established pattern: file written to `handoff/` and `.kilo/handoff/`; all root + `.kilo` + `.kilo/handoff` symlinks repointed at it.
- Did not run verification, modify experiments, change baselines, or take any research action beyond creating this handoff.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Do not invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # extended (~21 min)
SEED=42 python3 run_all_verification.py --full     # full (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
SEED=42 bash scripts/check.sh
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.
Durable copies written to: root, `handoff/`, `.kilo/handoff/`. Symlinks updated as applicable.

Handoff written by agent at 2026-11-04T12-53-38Z.
" \
  /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff/handoff_2026-11-04T12-53-38Z_INITIAL_TASK.md