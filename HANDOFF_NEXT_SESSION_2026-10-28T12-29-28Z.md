# Handoff for Next Agentic Work Session

**Created:** 2026-10-28T12:29:28Z
**Session Context:** Research phase complete (E001–E043). All experiments committed. Validated survivors documented in `ledger/RESEARCH_LEDGER.md`.

## Current State Summary

### Research Phase Status
- **Phase:** Complete (E001–E043 all run and documented)
- **Survivors:** 5 strategies pass gates (TSM pure, reversal 12m/10d, DN low-beta, DN low-vol, blend TSM+DN low-beta 50/50). All documented in `ledger/RESEARCH_LEDGER.md`.
- **Best market-neutral:** `blend_tsm_dnlowbeta` 50/50 — OOS Sharpe 1.625, β≈-0.05, turnover 6.4%, MaxDD -0.217 (E014). Simple `dollar_neutral_lowbeta` is validated keeper (Sharpe 1.287, z=7.10).
- **Baselines verified:** All `experiments/*.json` golden files are pinned in `ledger/golden_baseline.json`. Verification suite in working order.

### Key Technical State
- **Verification infrastructure:** `run_all_verification.py` (quick/extended/full modes), `scripts/check.sh`, golden baseline guards in place.
- **Data coverage enforced:** All driver data files pinned in `ledger/data_baseline.json`. E029 fundamentals pinned in `data/fundamentals/`. E030 ETF panel committed.
- **Optimizer notes:** SLSQP status-8 quirk fixed (validate on constraints, not status). Ill-conditioned QP still causes small numeric drift in E041/E042 grid artifacts (accepted in extended reports, do not re-pin).
- **Reproducibility:** Always use `SEED=42`. Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution, close-to-close v1.2.3 primary convention.

## Immediate Priority Task

**Optimize the TSM+DN blend weights (E015) and evaluate for additional diversification.**

This is the most valuable next step per `HANDOFF_NEXT_AGENT.md`. The current 50/50 blend achieves near-zero beta by accident (DN short leg offsets TSM long exposure), not by design.

### Concrete Actions

1. **Weight grid search for TSM/DN blend**
   - Test ratios: (0,100), (25,75), (50,50), (75,25), (100,0) of TSM/DN low-beta
   - Evaluate: OOS Sharpe, beta vs SPY, alpha, turnover, max DD, Calmar, performance in 2022 bear / COVID
   - Look for weights achieving |β| < 0.1 with Sharpe >= 1.65 or improved drawdowns
   - Consider risk-parity style allocation (equalize risk contributions)

2. **Document blend mechanics**
   - Analyze why 50/50 gives β≈-0.05; decompose beta contributions
   - Add explanation to results for reproducibility

3. **Explore third component (if promising)**
   - Consider pairs trading (Gatev et al. 2006) on large_liquid universe
   - Identify cointegrated pairs, test distance method with proper formation/trading windows
   - Require correlation < 0.3 to existing blend and positive marginal contribution
   - Must pass placebo validation if introducing new signal

4. **Register and document as E015**
   - Create `experiments/run_e015.py` following existing driver patterns
   - Output to `experiments/e015_*.json` with pre_registered block (gates, falsification, sensitivity)
   - Add entry to `ledger/RESEARCH_LEDGER.md` with clear keep/reject decision
   - Update verification if needed

### Success Criteria
- Identify blend weights with Sharpe ≥ 1.65 or materially better drawdown while maintaining |β| < 0.2 (prefer |β|<0.1)
- If third component added, show correlation < 0.3 to blend and positive contribution after costs
- All new results pass placebo validation
- Complete ledger entry with evidence

### Warnings / Constraints
- **Do not** modify or re-pin `experiments/*.json` golden files without explicit justification — verification restores them
- **Do not** re-pin baselines to silence numeric drift; see optimizer notes in AGENTS.md and ledger E049
- Always use `SEED=42`
- Follow cost model (tc=0.5bps + slippage=0.2bps), next-day open execution
- Market-neutral requires careful shorting-cost consideration
- Run `SEED=42 bash scripts/check.sh` before committing

## Quick Commands
```bash
# Integrity check
SEED=42 bash scripts/check.sh

# Quick verification (8 drivers)
SEED=42 python3 run_all_verification.py --quick

# Extended/full if needed
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Inspect current best strategies
cat ledger/RESEARCH_LEDGER.md | grep -n -A 30 "E014\|blend_tsm_dnlowbeta\|dollar_neutral_lowbeta"
```

## Key Files to Read First
- `ledger/RESEARCH_LEDGER.md` — full research history and current survivors
- `HANDOFF_NEXT_AGENT.md` — detailed rationale for this task
- `src/strategies.py` — strategy implementations (TSM pure, DN low-beta)
- `src/backtest.py` — backtest engine, weighting, costs
- `experiments/run_e014.py` — reference for blend implementation
- `AGENTS.md` — full reproducibility/baseline integrity rules
