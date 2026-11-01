# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T10:31:33Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

**Priority 1: Fix tangency QP ill-conditioning (E049 follow-up)**

The tangency QP in `src/portfolio_opt.py` `max_sharpe` branch remains ill-conditioned. SLSQP is sensitive to 1-ulp covariance perturbations and artifacts drift vs goldens (E041/E042). Do **not** re-pin to silence — fix the solver/path first.

### Verification (do first)
1. `pip install -r requirements.txt` if environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. If verification was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

### Work to do
1. Route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` active-set enumeration.
2. Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point (`src/portfolio_opt.py:492`).
3. Validate with `SEED=42 python3 experiments/run_e041.py` and `SEED=42 python3 experiments/run_e042.py --n-sim 50`; compare against committed goldens (expect reduced drift). Only re-pin artifacts deliberately if the fix is correct and justified.
4. Run full verification (`SEED=42 python3 run_all_verification.py --full` or `make verify-full`) to confirm stability.
5. Update `ledger/RESEARCH_LEDGER.md` (E049) with findings/fix summary.

## Quick references
- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions

(End of file)
