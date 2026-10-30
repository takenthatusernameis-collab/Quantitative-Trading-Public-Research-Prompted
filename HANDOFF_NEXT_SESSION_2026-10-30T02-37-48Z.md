# Handoff - 2026-10-30T02:37:48Z

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Phase: Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- Canonical artifacts: `experiments/*.json` (golden). Never modify without following `ledger/golden_baseline.json` re-pinning rules.
- Verification uses snapshot system in `.verify_snapshot/` (gitignored) with `ACTIVE.json` PID tracking. A killed run must be recovered.

## Current State
- Baseline integrity guards enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Data: cached in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`. Offline mode enforced in verification.
- Open items (see `ledger/RESEARCH_LEDGER.md`):
  - E049: Optimizer determinism - SLSQP status 8 handling fixed, but E041/E042 grid still show 29-133 numeric diffs (1-ulp sensitivity on ill-conditioned QP). Do not re-pin to silence.
  - E029/E030: Now offline-reproducible (pinned snapshots/panels).
  - Cache coverage: all driver data inputs must be tracked and pinned.

## Initial Task For Next Session
1. **Verify baseline integrity** (must be clean before any changes):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If it reports golden mismatch or pending snapshot, recover first: `SEED=42 python3 run_all_verification.py --restore-only`

2. **Run quick verification** to confirm reproducibility:
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Expect ~8 min. Do not commit if interrupted - restore goldens.

3. **Review open items**:
   - Read `ledger/RESEARCH_LEDGER.md` entries for E049 (optimizer determinism). Decide whether to investigate further or accept remaining numeric drift per ledger guidance.
   - Check `ledger/golden_baseline.json` and `ledger/data_baseline.json` are consistent with current goldens/data.

4. **Only commit if all checks pass**. If you must update a golden/data artifact, use the explicit `--update` flags on the check scripts and document in ledger. Never let verification re-pin baselines as a side effect.

## Notes
- Use `SEED=42` for all runs.
- Conventions: close-to-close v1.2.3 primary; overnight decomposition reported.
- Tests: `python3 -m py_compile` on changed files. Portfolio optimizer behavior is pinned by `tests/test_portfolio_opt.py`.
