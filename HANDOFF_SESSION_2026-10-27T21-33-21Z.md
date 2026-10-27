# Session Handoff — 2026-10-27T21:33:21Z

## Repository State

- **Research phase:** Complete (E001–E047). All published results documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** Clean at HEAD (on branch main). All tracked artifacts match `HEAD`.
- **Verification status:** `SEED=42 bash scripts/check.sh` passes. `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` both pass.
- **Time:** 2026-10-27T21:33:21Z

## Initial Task For Next Session

**No new implementation required.** The project is in a clean, verified, production-ready research state.

If a new task is explicitly assigned by the maintainer, only consider these bounded options:

- [ ] **CI Workflow (maintainer-gated)** — Create `.github/workflows/verification-gate.yml` from `.github/workflow-templates/verification-gate.yml` via GitHub UI (outside agent scope per `AGENTS.md`).
- [ ] **Environment-sensitive drift (E030/E041)** — Remain reporting-only (decisions unchanged: E030 REJECTED, E041 REJECTED 3/5). Investigate only in isolated copies; do **not** re-pin goldens to silence numeric drift.
- [ ] **Fundamentals snapshot regeneration (E029)** — If live yfinance refresh is required, follow `HANDOFF_CURRENT.md`. Only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit justification.

## Quick Verification Commands

```bash
# Full convention + golden checks
SEED=42 bash scripts/check.sh

# Explicit golden guards
python3 scripts/check_goldens_clean.py
python3 scripts/check_golden_baseline.py

# Recover from interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Constraints (Must Follow)

- **Seeds & vintages:** Always use `SEED=42`. Use pinned price cache (2026-10-12 vintage) and pinned fundamentals snapshot (2026-10-12).
- **Goldens are authoritative:** Never modify `experiments/*.json` unless doing a deliberate re-pin. Any re-pin must appear in diff via `python3 scripts/check_golden_baseline.py --update` with justification.
- **No goalpost moves:** Do not change tolerances, skip logic, driver behavior, or gates.
- **Crash-safety:** Never leave a verification run half-finished. Honor snapshot/restore. Restore before committing if interrupted.
- **Isolated runs for slow drivers:** Run E041, E042, and extended verification in isolated copies (not this repo) to avoid capturing output into canonical goldens.
- **Offline reproducibility:** `QUANT_RESEARCH_OFFLINE=1` enforced by suite. Missing data cache is a hard failure.

(End of file)
