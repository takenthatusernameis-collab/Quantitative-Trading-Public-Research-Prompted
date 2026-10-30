# HANDOFF - Next Agentic Session
Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 422f7fc chore(kilo): checkpoint agent session

## Project State
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All experiments are pre-registered with falsification expectations and promotion gates.
- Baseline integrity enforced via golden files in `experiments/` and SHA-256 checks in `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- Verification suite with backups in `.verify_snapshot/` (gitignored); guards against half-finished runs.

## Current Working Tree
- Modified (uncommitted): `scripts/__pycache__/*.pyc`, `src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc` (Python bytecode from prior runs)
- Clean of substantive code changes from this session start

## Quick Start / Verification
```bash
SEED=42 bash scripts/check.sh                    # fast convention-robustness + template validation
SEED=42 python3 run_all_verification.py         # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full  # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover from interrupted run
```
Key guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`. Never re-pin goldens as side effect of verification.

## Important Context (from AGENTS.md)
- Convention: close-to-close v1.2.3 primary; overnight decomposition reported.
- Data: cached parquet in `data/` (gitignored except pinned vintages). E029 fundamentals pinned in `data/fundamentals/`. Cache coverage enforced.
- Optimizer determinism (E049): solver status 8 treated as success if feasible/optimal; tangency QP ill-conditioned causes small numeric drift in E041/E042 grid (do not re-pin).
- Extended verification: 15/18 extended drivers reproduce exactly; E030/E029 offline-reproducible since 10/20; E041 has fixed structural issues but remaining numeric drift from ill-conditioned QP.
- Do not commit verification output. Restore goldens if interrupted.

## Next Agent Task
Leave a clear initial task message for the next agentic work session in a durable handoff.

### Suggested First Actions
1. Read `ledger/RESEARCH_LEDGER.md` to understand current research status and open items (e.g. E049 follow-ups).
2. Run `SEED=42 bash scripts/check.sh` to establish clean baseline state.
3. If investigating E041 numeric drift or optimizer behavior, review `src/portfolio_opt.py`, `tests/test_portfolio_opt.py`, and E041/E042 artifacts.
4. Follow repo conventions strictly - do not move goalposts, maintain pre-registration, respect golden file policy.

### Notes
- All handoff files are in repo root. This is a fresh timestamped handoff.
- Working directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- If environment is fresh, dependencies per `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).

**Initial Task Message (to paste/start):**
"Continue from this handoff. Verify repo state with `SEED=42 bash scripts/check.sh`. Review `ledger/RESEARCH_LEDGER.md` for open items (notably E049/optimizer determinism). Do not modify golden files or re-pin baselines unless explicitly justified and documented. Follow all constraints in AGENTS.md."
