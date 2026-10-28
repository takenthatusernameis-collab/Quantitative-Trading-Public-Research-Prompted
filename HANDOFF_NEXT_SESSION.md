# HANDOFF FOR NEXT AGENTIC SESSION

**Timestamp (UTC):** 2026-10-28T09:15:30Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** c4c942c (chore(kilo): checkpoint agent session)
**State:** Research phase complete through E018. E015 contamination corrected (multi-asset inflated by roll artifacts). Futures roll methodology + carry infrastructure in place.

---

## CURRENT STATE SUMMARY

- **Flagship (equities):** Pure TSM (12m lookback, inv-vol, monthly rebalance) on large_liquid — OOS Sharpe 2.141, cost-robust, low turnover. (E010/E015)
- **Market-neutral keeper:** Dollar-neutral low-beta sort — validated (Sharpe 1.287, z 7.78, β≈0), equity-specific. (E012/E013)
- **Best blend so far:** TSM + DN low-beta gave 1.625 but was suboptimal vs pure TSM; blend not promoted. (E014)
- **Futures sleeve:** Roll-corrected TSM-18m strongest on futures (0.805, z 3.76, bear +1.348, β -0.010) but below 1.0 gate. TSM-9m primary (0.680, z 3.33). Realized-roll-yield carry is near-significant (Sharpe 0.523, carry-specific z 2.65 < 3) with best bear profile (+0.907) and lowest turnover (3.1%) — rejected at pre-registered bar, retained as candidate. (E016-E018)
- **Key correction:** E015 multi-asset raw-stitched futures inflated result (2.086 → 1.838 with de-seamed). (E017)
- **Infrastructure:** `src/futures.py` (seam detection/de-seaming, normalized basis, realized roll yield), carry signal/weights, extended 16-contract futures panel (2014-2026) cached, placebo machinery (blended + carry-specific seam-calendar-preserving), replication anchors in place.

---

## TOP PRIORITY TASK (E019)

**Pre-registered cross-asset portfolio construction: (a) TSM+carry blend grid with fresh gates, (b) total-portfolio test of equity flagship + cross-asset futures sleeve.**

This is the highest-value open question. E018 disclosed non-official blend Sharpes (0.70-0.82) in a debug run but gates must be set fresh and falsification must beat the BEST pure variant (TSM-18m 0.805), not TSM-9m.

### Pre-register before running
- **Blend gates:** OOS Sharpe >= 0.8, blended-placebo z >= 3, positive bear Sharpe, |β| <= 0.2, turnover <= 0.08. **Falsification:** best blend must beat **TSM-18m (0.805)** on OOS Sharpe.
- **Total-portfolio gates:** total OOS Sharpe >= 2.0 AND bear-market Sharpe **strictly greater** than equity-only flagship's, at chosen futures weight.
- **Disclose execution mismatch:** equity sleeve next-day-open vs futures sleeve close-to-close (mixing conventions). Document caveat.

### Concrete steps
1. **Create driver** `experiments/run_e019.py` following `run_e018.py`/`run_e017.py` style. Record all gates in docstring + JSON.
2. **Blend grid:** TSM(18m, symmetric, inv-vol, de-seamed) + carry(252d, realized roll yield) on extended 16-contract futures panel (2014-2026), monthly rebalance, next-day-open, tc 0.5bps+slippage 0.2bps. Weights: TSM {0.3, 0.5, 0.7}, carry = 1-TSM. Use blended placebo (random TSM + random carry) for z-scores.
3. **Total-portfolio test:** Equity flagship (pure TSM 12m, long-only, inv-vol, large_liquid) + futures sleeve (TSM-18m symmetric, de-seamed). Weights {equity 0.75/futures 0.25, 0.5/0.5, 0.25/0.75}. Compute total returns with documented execution convention mix. Compare to equity-only (Sharpe 2.141) and require bear Sharpe improvement.
4. **Report honestly:** Full grid for both families. If either passes gates → promote and update README/ledger. If both fail → record negative and pivot to new strategy family per E016 search order (stat-arb/pairs Gatev et al. 2006, variance risk premium, macro momentum).
5. **Record** E019 in `ledger/RESEARCH_LEDGER.md` with tables matching prior format, update `README.md`, commit.

### Key references
- Handoff: ledger lines ~1261-1349 (post-E018)
- Artifacts: `experiments/run_e018.py`, `experiments/e018_carry_validation.json`, `experiments/run_e017.py`, `experiments/e017_extended_futures.json`, `src/futures.py`
- Data: extended 16-contract futures panel cached in `data/`, `large_liquid` equities cached

---

## DO FIRST (verification)
Run these to confirm environment is clean and baselines reproduce:
```bash
SEED=42 python3 -m py_compile src/futures.py src/strategies.py src/backtest.py src/data.py src/validation.py
SEED=42 python3 experiments/run_e017.py  # should reproduce E017 numbers
SEED=42 python3 experiments/run_e018.py  # should reproduce E018 numbers
SEED=42 bash scripts/check.sh  # convention checks + py_compile + tests
```
Note: verification suite may overwrite/restore experiments; follow AGENTS.md baseline integrity rules. Don't re-pin goldens unless explicitly required and justified.

---

## NOTES & CAVEATS
- **Multiple testing:** Two families in one experiment. Pre-register all gates before inspection.
- **Execution mismatch:** Total portfolio mixes next-day-open (equities) and close-to-close (futures). Document, don't ignore.
- **Bear regimes:** Only 2-3 true bear regimes in 42 folds; bear-Sharpe gates are noisy.
- **Carry:** Near-miss (z 2.65) but rejected at bar. Don't resurrect without fresh pre-registration.
- **Roll artifacts:** Always use de-seamed futures. E015 correction is critical.
- **Goalposts:** Do not move gates post-hoc. Report full grids.

**Start with E019 pre-registration in the driver, then run the blend grid, then total-portfolio test.**
