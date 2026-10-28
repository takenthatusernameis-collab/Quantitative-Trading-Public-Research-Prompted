# HANDOFF - Next Agentic Work Session
Timestamp (UTC): 2026-10-28T18-28-05Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 65225dd
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All goldens are the committed baselines (`experiments/*.json`). Verification suite backs up/restores them.
- Working tree state: checked at handoff time.
- No active `.verify_snapshot/` — nothing to recover.
- Pinned data: `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Cache coverage enforced by `scripts/check_data_coverage.py`.
- Optimizer determinism note (E049): solver status not used for gating; tangency QP remains ill-conditioned (small numeric drift possible). Do not re-pin goldens to silence drift.

## Clear Initial Task (Execute in Order)
Treat any failure as a blocker. Follow recovery procedures before making changes.

### 1) Confirm clean baseline
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
python3 -m unittest tests.test_portfolio_opt
```
All checks must pass. `scripts/check.sh` runs py_compile, JSON validation, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, experiment imports, and portfolio_opt tests.

### 2) Run quick verification (~8-10 min)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted, recover:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```
Or restore from git if needed: `git checkout -- experiments/` (use pinned commit if HEAD already contains a captured run).

### 3) Review open items & context
- Read `ledger/RESEARCH_LEDGER.md` (focus: E049, E041, E042-lead, E042 primary, E048, E045–E048)
- Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` before any intentional re-pinning
- No new research warranted unless explicitly requested. Baseline guards are strict; never re-pin goldens to silence drift.
- E041 numeric drift (133 diffs) due to 1-ulp sensitivity; do not silence by re-pinning.
- Ledger inconsistency to resolve via verification: E048 says E042-lead is unfixed/breaks primary gate; E049 says fixed. Authoritative check is `run_all_verification.py` itself.

## Notes
- Do not commit verification output. If a run is interrupted, restore goldens before committing.
- Extended verification: `SEED=42 python3 run_all_verification.py --extended` (~21 min). Full: `--full` (~15 min). Only run if explicitly needed.
