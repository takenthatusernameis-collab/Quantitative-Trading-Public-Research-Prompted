# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T15:12:48Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ HEAD
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## INITIAL TASK MESSAGE FOR NEXT SESSION

```
START HERE:

1) VERIFY CLEAN BASELINE (must pass)
   - pip install -r requirements.txt  (if needed)
   - SEED=42 bash scripts/check.sh  (expect EXIT 0, "=== All checks passed ===")
   - git status --short  (only __pycache__/*.pyc acceptable)
   - Check for stale snapshot: .verify_snapshot/ACTIVE.json — remove if present with no live run
   - If artifacts modified by interrupted run: SEED=42 python3 run_all_verification.py --restore-only

2) IF BASELINE CLEAN, TACKLE E049 (highest priority)
   - Fix tangency QP ill-conditioning in src/portfolio_opt.py max_sharpe branch
   - Route max_sharpe through exact_qp/exact_tangency_kkt active-set enumeration
   - Fix start point y0 = w_feas / max(mu_s'w_feas, 1e-12) at src/portfolio_opt.py:492
   - Preserve solver-status independence (validate on constraints, not scipy status) — tests/test_portfolio_opt.py guards
   - Re-run affected drivers with QUANT_RESEARCH_OFFLINE=1; aim to reduce drift in E041/E042 within tolerance
   - DO NOT re-pin artifacts to silence; document changes in ledger/RESEARCH_LEDGER.md

3) REPORT STATUS
   - After check.sh passes or after E049 changes, summarize baseline state and any ledger updates.
```

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md` (E044–E049)
- **Baselines:** `experiments/*.json` canonical goldens pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`
- **Offline reproducible:** E029, E030 (run with `QUANT_RESEARCH_OFFLINE=1`)
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` must all pass

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — commands & conventions

(End of file)
