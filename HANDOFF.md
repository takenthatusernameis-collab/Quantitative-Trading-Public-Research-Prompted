# HANDOFF — 2026-10-28T10:25:29Z

## Current State
- **Research complete**: E001–E043 finished. Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Goldens are canonical**: All committed artifacts in `experiments/*.json` are the authoritative baseline. The verification suite backs up/restores them and must never be left half-finished.
- **Safeguards active**: `.verify_snapshot/` (with `ACTIVE.json` PID tracking), `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and `scripts/check_data_coverage.py` are enforced.
- **Reproducibility notes**: E029 and E030 are now offline-reproducible with 0 differences in `--extended`. E041 optimizer-drift remains open (133 numeric differences > 1e-4 tolerance) despite structural issues being fixed (see E049).

## Immediate Task For Next Session
**Verify baseline integrity first. Do not re-run the full verification suite to "refresh" goldens.**

1. **Confirm clean state** (fast):
   ```bash
   SEED=42 bash scripts/check.sh
   # or
   make check
   ```
   This runs py_compile, convention checks, `check_goldens_clean.py`, `check_golden_baseline.py`, and `tests/test_portfolio_opt.py`.

2. **If `check.sh` reports issues**:
   - If snapshot is stale → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
   - If goldens differ from `ledger/golden_baseline.json` → do **not** re-pin via the verification suite. Only re-pin with `python3 scripts/check_golden_baseline.py --update` if explicitly justified and documented.
   - If data coverage fails → commit missing files and re-pin with `python3 scripts/check_data_coverage.py --update`.

## Known Open Items
- **E041 (market-neutral portfolio)**: Optimizer now validates on constraints (not solver status), fixing structural drift. Remaining 133 numeric diffs are 1-ulp sensitivity of an ill-conditioned tangency QP. Do **not** silence by re-pinning — tracked in `ledger/RESEARCH_LEDGER.md` E049.
- **CI workflow**: `.github/workflows/verification-gate.yml` cannot be created by agents (controller restores workflows; token lacks `workflows` permission). Use `.github/workflow-templates/verification-gate.yml` as template.

## Quick Repro Commands
```bash
SEED=42 python3 run_all_verification.py           # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # extended (~21 min)
SEED=42 python3 run_all_verification.py --full     # full (~15 min)
```

**Rule:** Treat committed `experiments/*.json` as the record. Any change to data, drivers, or optimizer logic must preserve baseline integrity or be explicitly re-pinned with ledger updates.
