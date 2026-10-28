# HANDOFF - Timestamped Initial Task Message for Next Agentic Work Session

**Created:** 2026-10-28T01:44:09Z
**Session:** Initial task request - "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/State:** Research phase complete (E001–E043). Surviving strategies documented in ledger/RESEARCH_LEDGER.md

## Context
- Research phase complete. Portfolio-construction closed (E042/PARTIAL, E042b REJECTED).
- E049 fixed solver-exit-status branch selection in `src/portfolio_opt.py` (max_sharpe tangency) and added `tests/test_portfolio_opt.py`.
- E042-lead primary block now reproduces committed golden to ~5e-9; lead artifact's `/placebo_constrained` block was deliberately re-pinned (visible in diff).
- Primary verification gate is green again.
- Open item: tangency QP still ill-conditioned (1-ulp moves answers) — E041/E042 grid artifacts still drift (29-133 diffs) due to conditioning, not fixed. Also a smaller start-point issue in optimizer left unfixed by design.

## High-Priority Next Task (Concrete, Pre-Registered)
**Tackle optimizer ill-conditioning for tangency/max_sharpe QP to make E041/E042 artifacts bit-reproducible across environments.**

### Goal
Replace/robustify the SLSQP-based tangency solve so answers don't depend on floating point/BLAS/build details. Make affected artifacts reproducible (byte-identical excluding timestamp/runtime) without changing research decisions/gates.

### Scope
- Focus on `src/portfolio_opt.py` max_sharpe/tangency path (and placebo projection consistency).
- Consider exact active-set enumeration for small KKT sets (N<=5) as reference/oracle (ledger notes feasibility), or a more stable solver formulation.
- Fix the start-point issue noted (`y0 = w_feas / max(mu_s'w_feas, 1e-12)`) if it can be done without changing published numbers? Or handle deliberately with re-pinning if necessary.
- Add/strengthen tests (extend `tests/test_portfolio_opt.py`).
- Re-pin affected artifacts deliberately with justification if numbers change (follow E046/E048/E049 precedent). Never re-pin as side effect of verification.

### Specific Files to Touch
- `src/portfolio_opt.py` (tangency solve, feasibility, start point)
- `tests/test_portfolio_opt.py` (extend)
- Possibly `experiments/run_e041.py`, `experiments/run_e042*.py` if needed
- Artifacts: `experiments/e041_*.json`, `experiments/e042_*.json` if re-pinned

### Verification
- Run `SEED=42 python3 experiments/run_e041.py` and compare to committed goldens (expect drift reduction).
- Run `SEED=42 python3 experiments/run_e042.py --n-sim 50` (must remain byte-identical excluding timestamp).
- Run `SEED=42 python3 experiments/run_e042_lead.py` (must remain byte-identical excluding timestamp/runtime).
- Run `SEED=42 make check` and/or `SEED=42 python3 run_all_verification.py` (primary gate).
- If re-pinning needed: use `python3 scripts/check_golden_baseline.py --update` and document in ledger.

### Constraints (Must Follow)
- SEED=42 always. No goalpost moves, no gate/threshold changes, no research decisions changed.
- Golden artifacts are canonical - never modified by verification suite.
- Follow baseline integrity rules (check_goldens_clean/golden_baseline, snapshot/recover).
- Offline reproducible with pinned vintages (2026-10-12 primary).
- Convention v1.2.3: c2c primary, overnight decomposition mandatory.
- Do not create `.github/workflows/` (CI template exists).
- Pre-registration discipline, no tolerance/driver/skip changes without strong justification.

## Secondary Tasks (If Time)
- Address the small start-point defect carefully (could change numbers) - only if paired with deliberate re-pin + ledger entry.
- Investigate any remaining extended-verification drift beyond conditioning.
- Clean up any stale `.verify_snapshot/` if present.

## Quick Commands
```bash
SEED=42 make check                    # fast checks
SEED=42 python3 run_all_verification.py  # primary (~8 min)
SEED=42 python3 run_all_verification.py --extended  # full drift scan (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens
```

## References
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049 details, open item)
- AGENTS.md: baseline integrity, reproducibility, verification commands
- README.md: final status and convention policy
- Tests: `tests/test_portfolio_opt.py`
