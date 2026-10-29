# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T18:41:38Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**HEAD:** `24ead54` chore(kilo): checkpoint agent session
**Working tree:** clean checkpoint state (see recent kilo agent commits)
**Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`

## Clear Initial Task
**Objective:** Establish a clean, verified baseline before starting any new work.

### Priority 1: Baseline Integrity (BLOCKING)
Before making any changes:
1. Verify no verification run is in progress or left half-finished.
2. Ensure goldens match HEAD and the pinned baseline.
3. Confirm data cache coverage is intact.

**Commands:**
```bash
git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted status --short
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
```

If `scripts/check.sh` reports a golden mismatch:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or git checkout -- experiments/
```
Do **not** re-pin goldens to silence drift. Only re-pin via `python3 scripts/check_golden_baseline.py --update` if there is an explicit, justified reason (and it will appear in diff).

### Priority 2: Review Open Items
Read the ledger for active constraints:
- `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned QP). The extended verification may report E041 drift (133 numeric differences remain). **Do not re-pin E041/E042 grid artifacts.**
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` — know what is pinned.
- `data/fundamentals_vintages.json` and `data/vintages.json` — confirm offline reproducibility assumptions.

### Priority 3: Define Next Action
After baseline is clean:
- If the user has specified a new experiment, follow `AGENTS.md` pre-registration rules (docstring + pre_registered block, gates, falsification, sensitivity grid).
- If unclear, propose 1-2 concrete next steps based on ledger gaps and wait for direction.
- Follow multiple-testing discipline: grids are "reported, not gated"; confirmatory runs need full placebo.

## Quick Context
- Convention: close-to-close v1.2.3 primary; overnight decomposition reported
- Seed: always `SEED=42`
- Verification: `verify-quick` (~8 min), `verify-extended` (~21 min), `verify-full` (~15 min)
- Data: cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned. Cache coverage is enforced.
- Optimizer: solver exit status not gated (scipy SLSQP status 8 acceptable if feasible/optimal) — enforced by `tests/test_portfolio_opt.py`

## First Action (explicit)
Run baseline integrity checks (Priority 1). Report results in a concise summary. If clean, state "Baseline clean" and propose next action. If not, restore and re-check.
