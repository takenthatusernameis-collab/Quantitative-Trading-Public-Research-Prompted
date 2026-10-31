# Handoff — 2026-10-31T22:39:56Z

## Initial task for the next agentic session
**Objective:** Establish a clean, verifiable baseline before making any changes. Treat the committed artifacts as authoritative and do not mutate goldens as a side effect of verification.

## Current repo state
- Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical experiment outputs live in `experiments/*.json` (goldens).
- Data baselines/pins: `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`.
- Verification infrastructure: `scripts/check.sh`, `run_all_verification.py`, `verify_convention_robustness.py`
- Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Snapshot/recovery: `.verify_snapshot/` (gitignored) with `ACTIVE.json` for live-run ownership; use `run_all_verification.py --restore-only` to recover.

## Recommended first steps (in order)
1. **Check working tree / baseline hygiene**
   - `git status --short`
   - If goldens look modified by a prior interrupted run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` as appropriate). If `HEAD` already captured a run, restore from the commit that matches `ledger/golden_baseline.json` instead.

2. **Fast integrity check (offline, seconds)**
   - `SEED=42 bash scripts/check.sh`
     This runs py_compile, template validation, convention-robustness, and the golden/data baseline guards. Treat any failure here as blocking.

3. **Decide verification scope**
   - Quick repro check: `SEED=42 python3 run_all_verification.py --skip-slow` (or `make verify`)
   - If you need full coverage of committed drivers: `SEED=42 python3 run_all_verification.py --extended` (reporting only via `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, never written under `experiments/`)
   - Only run `--full` if explicitly needed (larger cost).

4. **Read context for open items**
   - Review `ledger/RESEARCH_LEDGER.md` (pay particular attention to E041 optimizer determinism / ill-conditioned tangency QP, E048 cache coverage enforcement, E029/E030 offline reproducibility).
   - Review `tests/test_portfolio_opt.py` (solver-status gating rule is pinned here).

## Hard constraints (do not violate)
- **Never mutate goldens via verification.** The suite backs up/restores `experiments/`. Do not re-pin baselines as a side effect of a routine run.
- **Re-pinning requires intent.** To change a pinned baseline, use the explicit update flags (e.g. `scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`) and only do so with justification captured in the ledger/diff.
- **Offline-first for verification.** The suite runs with `QUANT_RESEARCH_OFFLINE=1`. Any new data dependency must be committed and pinned via the data coverage guard.
- **No workflow creation.** `.github/workflows/` cannot be created/modified by automated agents; use `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md` if needed.
- **Pre-registration discipline.** Do not move goalposts post-hoc. Sensitivity grids are reported, not gated.
- **Optimizer rule.** Validate solver answers against problem constraints, not solver exit status (SLSQP status 8 can be benign).

## Key pointers
- `AGENTS.md` — full commands, conventions, and reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — research history, decisions, open items
- `ledger/golden_baseline.json` / `ledger/data_baseline.json` — pinned fingerprints
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py` — optimizer determinism
- `run_all_verification.py` — orchestration, backup/restore, drift reporting

**Next action:** Start at step 1 above. If baseline is already clean and verified, summarize state and await explicit direction before expanding scope beyond verification/integrity work.