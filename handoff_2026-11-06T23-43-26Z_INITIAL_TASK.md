# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-06T23-43-26Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 8b4d056
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- No active verification run; `.verify_snapshot/` absent.
- **Working tree is not clean** (12 modified tracked `__pycache__/*.pyc` files under `scripts/`, `src/`, `tests/`). These are compiled-bytecode artifacts, not `experiments/*.json` goldens and not data-baseline inputs. No `experiments/*.json` changes detected at handoff creation.
- No research actions taken in this session beyond creating this handoff.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Inspected repo state (`git status`, latest handoff) and created this durable timestamped handoff.

## Initial Task (clear)

**Do not invent a research task or run verification unprompted.**

1. Inspect the actual repository state and understand why tracked `__pycache__/*.pyc` files are modified:
   - `git status --short`
   - `git diff --name-status`
2. Verify the research integrity baselines are intact before any new work:
   - `SEED=42 bash scripts/check.sh` (convention/golden/data/template checks)
   - If a golden mismatch is reported, restore/fix **before** committing (`SEED=42 python3 run_all_verification.py --restore-only` or targeted `git checkout <commit> -- experiments/<file>` per `ledger/golden_baseline.json` guidance).
3. Resolve the `__pycache__` modifications only if appropriate for the repo conventions (do **not** blindly commit generated artifacts; determine whether they should be restored, ignored, or handled per project policy).
4. Per `PROMPT.MD`, select and execute the highest-value next research task (discover/reproduce/validate a quantitative strategy), with pre-registration/falsification gates as required. Record evidence honestly.
5. End the session with a new durable, timestamped handoff describing state, actions, results, and the next clear task.

## First Commands

```bash
git status --short
git diff --name-only
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Key Constraints (AGENTS.md)

- `experiments/*.json` are committed goldens — never commit verification output or leave a run half-finished. Committed golden is authoritative; never re-pin to silence drift without following the re-pinning process.
- Golden baseline: `ledger/golden_baseline.json` (`scripts/check_golden_baseline.py`). Data coverage: `ledger/data_baseline.json` (`scripts/check_data_coverage.py`).
- Always use `SEED=42`. v1.2.3 primary convention is close-to-close.
- Verification runs overwrite/restore goldens; if interrupted recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- CI workflow cannot be created by automated agents; use local `make check/verify/*`.

## Handoff Provenance

Durable copies: `handoff/handoff_2026-11-06T23-43-26Z_INITIAL_TASK.md` and root `handoff_2026-11-06T23-43-26Z_INITIAL_TASK.md`.
Root convenience symlinks updated: `INITIAL_TASK.md`, `NEXT_HANDOFF.md`, `LATEST.md`, `handoff.md`, `next_session.md`, `next_session_handoff.md`.
