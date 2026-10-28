# HANDOFF — Timestamped initial task for next agentic work session

**Created:** 2026-10-28T07:39:11Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main`
**HEAD:** `0cf61a9` ("chore(kilo): checkpoint agent session")
**Working tree:** clean (verified `git status --short` empty; only `__pycache__/*.pyc` gitignored noise)
**Verify snapshot:** none active (`.verify_snapshot/` absent, no `ACTIVE.json`)

---

## INITIAL TASK (Clear & Actionable)

**PRIMARY OBJECTIVE:** The repository is in a verified-clean, reproducible state. The research phase (E001–E049) is complete and the novelty search is closed. There is **no outstanding bounded research task** — the highest-value remaining work is the **open engineering item flagged in the ledger (E049, "Open item — the QP is still ill-conditioned")**: replace the SLSQP tangency-QP solves in `src/portfolio_opt.py` with a well-conditioned, deterministic solver, then deliberately re-pin the affected E041/E042 artifacts.

### Immediate Actions (Do First)

1. **Confirm the clean state** (already done this session; re-verify cheaply):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Must pass all guards (goldens clean, golden baseline pinned, data coverage, JSON artifacts, portfolio optimizer tests).
   - Working tree must be clean relative to HEAD for tracked artifacts (`git status --short` empty).

2. **Re-read the open item** at the end of `ledger/RESEARCH_LEDGER.md` (E049, "Open item — the QP is still ill-conditioned"). It is the only ledgered, unresolved, bounded task. Do **not** re-pin E041/E042 artifacts until the solver defect is fixed — re-pinning now would bake this machine's numbers over an unfixed defect.

3. **If you choose not to pursue the QP work**, the repository is already complete and self-describing: leave the tree clean, do not commit, and report "no outstanding task" rather than inventing new research.

### Context

- **Convention:** Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside. Mixed-convention portfolios are prohibited.
- **Seeds:** Always use `SEED=42`.
- **Golden files:** `experiments/*.json` are canonical. The committed golden is the authoritative record, never the latest re-run. Re-pinning is deliberate (`python3 scripts/check_golden_baseline.py --update`) and must be visible in the diff.
- **Data:** Pinned vintages in `data/vintages.json` (`2026-10-12`) and `data/fundamentals_vintages.json`; the `2026-10-11` vintage is committed because several drivers request that end date explicitly. Cache coverage is an enforced invariant (`scripts/check_data_coverage.py`).
- **Optimizer:** SLSQP status 8 ("Positive directional derivative for linesearch") is acceptable when the returned point is feasible and optimal — `tests/test_portfolio_opt.py` (a first-class step of `scripts/check.sh`) pins this invariant. The tangency QP remains ill-conditioned (1-ulp input perturbation moves `min_var` answers by ~1e-05); this is the documented open item.
- **Verification suite:** `SEED=42 python3 run_all_verification.py` (quick, the enforced CI gate) is 100% PASS. `--extended` (~21 min) reports E029/E030/E041 as drifting (documented, accepted, no goldens modified).

### Success Criteria

- [ ] `scripts/check.sh` passes completely
- [ ] Working tree clean relative to HEAD for tracked artifacts
- [ ] No stale snapshots in `.verify_snapshot/`
- [ ] The E049 open item either (a) resolved with a deterministic solver + deliberate re-pin, or (b) explicitly declined with a recorded reason
- [ ] No new strategy family introduced, no goalpost moved, no committed golden silently replaced

## Notes

- **Do not commit** unless explicitly asked. Checkpoint commits are the session's convention, but only create them when there is a real state change to capture.
- **Do not re-pin** artifacts to silence known numeric drift (E041) — follow ledger guidance.
- Extended verification is slow (~21-40 min); only run if specifically needed.
- The research ledger (`ledger/RESEARCH_LEDGER.md`) is the single source of truth for all 49 experiments, their pre-registered gates, falsification expectations, and decisions. Read it before proposing any new experiment.

**Next agent:** Start with step 1 above. Report findings before taking further action.

(End of file - total 71 lines)