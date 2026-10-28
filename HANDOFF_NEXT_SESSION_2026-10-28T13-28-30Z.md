# HANDOFF: Next Agentic Work Session

**Timestamp:** 2026-10-28T13:28:30Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main @ 293087c (up to date with origin/main)
**State:** Research phase complete (E001–E043). All experiment lines closed:
- E041 max_sharpe blend: REJECTED 3/5 (E042 lead), market-neutrality fails G3.
- E042 min_variance blend (β cap 0.05): PARTIAL (4/5) — G1/G3/G4/G5 PASS, G2 β-constrained placebo z 2.11 < 3.0 FAIL. Market-neutral-total-portfolio line **CLOSED**.
- E042b max_sharpe β≤0.1 63d macro_inclusive_3: REJECTED 4/5 (G2 z 1.64 FAIL).
Surviving edges remain the component strategies (equity TSM flagship, DN low-beta sort, futures TSM 18m, futures realized-roll-yield carry, macro momentum).

## INITIAL TASK (CLEAR)
**Objective:** Establish a clean baseline, confirm the expected verification failure, then investigate the highest-value open item — the ill-conditioned `max_sharpe` tangency QP in `src/portfolio_opt.py` (decide artifact vs solver authority; research decision, NOT a mechanical repair).

## IMMEDIATE ACTIONS (do in order)
1. **Verify repo integrity**
   `SEED=42 bash scripts/check.sh`
   Expected: `check_goldens_clean.py` clean vs HEAD (only `__pycache__` `.pyc` diffs, untracked); `check_golden_baseline.py` clean; `check_data_coverage.py` clean; py_compile + tests green.
   Expected primary-gate failure: `run_all_verification.py` quick block likely reports `OVERALL: FAILURES DETECTED` due to `max_sharpe` tangency-QP drift (E048/E049 open item). This is **known** — do not treat it as new breakage to "fix by re-pinning".
2. **Restore if needed**
   If a verification run left artifacts modified, run `SEED=42 python3 run_all_verification.py --restore-only`. Ensure no stale `.verify_snapshot/ACTIVE.json` (none present now).
3. **Read the ledger open items**
   `ledger/RESEARCH_LEDGER.md`:
   - E049 root-cause section (solver exit status, not data) ~lines 4805-4845
   - "Open item — ill-conditioned max_sharpe QP" ~lines 4770-4783 (highest-value open item; breaks the primary gate)
   - "Open item — E041 is not explained by this defect" ~lines 4785-4793 (leave E041 as-is)
   - v1.2.7 standing rule: artifact-vs-code reconciliation; assert gate outcomes, not fixed stochastic constants.
4. **Execute the open item**
   Investigate `src/portfolio_opt.py` max_sharpe branch (`min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`, SLSQP ftol=1e-12): flat/near-degenerate feasible set lets the solver settle in different local optima. Decide whether the *committed artifact* or the *solver* is authoritative — that is a research decision. Document any conclusion in the ledger; do not move gates/thresholds/goalposts.
5. **Handoff again**
   After acting, write a new `HANDOFF_NEXT_SESSION_<timestamp>.md` and repoint `HANDOFF_CURRENT.md` / `HANDOFF_NEXT_SESSION.md` to it.

## CONSTRAINTS / NOTES
- **Goldens are authoritative:** `experiments/*.json` committed are the record. Never re-pin to silence numeric drift from ill-conditioned solvers (E049). `check_golden_baseline.py --update` only with explicit justification.
- **Offline-first:** `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard. Data vintages pinned (`2026-10-12` + `2026-10-11`; E029 fundamentals separately pinned).
- **Determinism:** Always `SEED=42`. Pre-registration + multiple-testing discipline; grids reported, not gated.
- **No half-finished verification:** never leave a verification run interrupted; check `check_goldens_clean.py` first.
- **No commits unless explicitly asked.**

## ARTIFACTS TO CHECK
- `ledger/RESEARCH_LEDGER.md` (open items, source of truth)
- `AGENTS.md` (commands, baseline integrity, reproducibility)
- `src/portfolio_opt.py` (max_sharpe tangency QP — open item)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `.verify_snapshot/` (must not contain `ACTIVE.json` when clean)
- `experiments/` (goldens; only `__pycache__` should be dirty)

**End of handoff. Proceed with step 1.**
