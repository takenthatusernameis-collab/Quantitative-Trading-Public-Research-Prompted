# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T10:27:20Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

No new task requested — leave the standing E049 follow-up (tangency QP ill-conditioning) as the initial task for the next session.

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, address the open item below.

## Open item (highest value)

Tangency QP in `src/portfolio_opt.py` `max_sharpe` branch still ill-conditioned (SLSQP at `ftol=1e-12`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs. **Do not re-pin to silence.** Route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` active-set enumeration, fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point (`src/portfolio_opt.py:492`), then re-pin affected artifacts deliberately. See `ledger/RESEARCH_LEDGER.md` E049.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions

(End of file)
