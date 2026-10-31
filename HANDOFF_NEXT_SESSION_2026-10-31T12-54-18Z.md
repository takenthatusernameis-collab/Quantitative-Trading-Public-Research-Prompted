# HANDOFF: Next Session (2026-10-31T12:54:18Z)

**Repo:** Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
**Seed:** Always use `SEED=42`
**Focus:** Baseline integrity → verification readiness (do not modify canonical goldens)

## Immediate Initial Task (in order)
- [ ] **Check for stale/interrupted verification**
  Look for `.verify_snapshot/ACTIVE.json`. If present, do not start a new run. Recover first.
- [ ] **Verify golden integrity (hard gates)**
  ```bash
  SEED=42 python3 scripts/check_goldens_clean.py
  SEED=42 python3 scripts/check_golden_baseline.py
  SEED=42 python3 scripts/check_data_coverage.py
  ```
- [ ] **Run fast convention check**
  ```bash
  SEED=42 bash scripts/check.sh
  ```
- [ ] **If anything is dirty from a prior interrupted run, restore before committing**
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  # or: git checkout -- experiments/
  ```

## Known Constraints (do not violate)
- **Goldens are canonical.** `experiments/*.json` must match HEAD or the pins in `ledger/golden_baseline.json`. Never re-pin as a side effect of running verification (`scripts/check_golden_baseline.py --update` is manual and must be intentional).
- **Data is pinned/offline-enforced.** All driver data must be git-tracked and present per `ledger/data_baseline.json`. `QUANT_RESEARCH_OFFLINE=1` is used by the suite; missing coverage fails hard.
- **Optimizer determinism (E049).** E041/E042 can show numeric drift (ill-conditioned QP). The solver-status gate was fixed (validate against constraints). Do **not** re-pin to silence known drift.
- **Extended reproducibility notes:** E029/E030 now offline-reproducible with pinned inputs; E041 still shows bounded numeric drift (reported, not gated).
- **CI workflow:** Cannot be created by agents (controller restores `.github/workflows/`). Template at `.github/workflow-templates/verification-gate.yml`.

## Quick Verification Options
- `make check` / `SEED=42 bash scripts/check.sh` (~seconds)
- `make verify-quick` / `SEED=42 python3 run_all_verification.py` (~8 min)
- `make verify-extended` / `SEED=42 python3 run_all_verification.py --extended` (~21 min)
- `make verify-full` / `SEED=42 python3 run_all_verification.py --full` (~15 min)

## Handoff Notes
- Read `AGENTS.md` for full details on recovery, drift reporting (`.verify_reports/` gitignored), and driver coverage.
- Read `ledger/RESEARCH_LEDGER.md` for experiment status and open items.
- If starting new work, keep changes scoped and re-run `scripts/check.sh` before committing.
