# HANDOFF - 2026-10-28T12-24-54Z

## Initial task for next agentic session
- **Goal:** Start from a clean verified baseline and only act on explicit user priorities.
- **Context:** Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered with falsification expectations and promotion gates.
- **First checks (required):**
  1. Run `SEED=42 bash scripts/check.sh` to validate conventions and golden baseline integrity.
  2. If `scripts/check_goldens_clean.py` or `scripts/check_golden_baseline.py` report issues, restore goldens before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate).
  3. Confirm `ledger/golden_baseline.json` matches current tracked `experiments/*.json` SHAs.
  4. If verification artifacts are in flux, ensure no active `.verify_snapshot/` exists (if present and stale per `ACTIVE.json`, recover per AGENTS.md).
- **Notes:**
  - Never modify `experiments/*.json` as a side effect of verification runs; the suite backs up/restores them.
  - Cache coverage is enforced (`scripts/check_data_coverage.py`) — missing/pinned inputs are required.
  - Follow AGENTS.md conventions strictly (seeds, pre-registration, multiple-testing discipline).
  - Do not commit verification output. If interrupted, restore with `--restore-only`.
  - Treat committed goldens as authoritative; re-pinning requires `check_golden_baseline.py --update` with justification.
- **Next steps:** Report baseline status (PASS/FAIL + details). Only proceed with new work after a clean baseline, and strictly per the user's explicit priorities.

## Durable handoff
This file: `HANDOFF_NEXT_SESSION_2026-10-28T12-24-54Z.md` (also symlinked as `HANDOFF_CURRENT.md` and `HANDOFF_NEXT_SESSION.md`).

## Verified state at handoff time (2026-10-28T12-24-54Z)
- HEAD: 2aa61bd
- Branch: main
- Working tree: has uncommitted tracked changes
- Snapshot: no active snapshot
