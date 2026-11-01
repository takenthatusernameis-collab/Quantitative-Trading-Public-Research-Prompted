# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T15:08:55Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ HEAD
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

**PRIORITY 1: Verify clean baseline**

1. If environment was reset, `pip install -r requirements.txt`
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ==="
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. If interrupted verification left artifacts modified, recover with `SEED=42 python3 run_all_verification.py --restore-only`
4. Confirm no stale snapshot: check for `.verify_snapshot/ACTIVE.json` — if present and no live run, remove it

**PRIORITY 2: Address E049 follow-up (highest value)**

The tangency QP in `src/portfolio_opt.py` `max_sharpe` branch remains ill-conditioned. E041/E042 grid artifacts and E042-primary still drift vs goldens (29–133 diffs). Do **NOT** re-pin to silence.

Tasks:
1. Route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` active-set enumeration
2. Fix the start point `y0 = w_feas / max(mu_s'w_feas, 1e-12)` at `src/portfolio_opt.py:492` (or equivalent)
3. Ensure solver-status independence is preserved (validate on problem constraints, not scipy exit status) — `tests/test_portfolio_opt.py` guards this
4. Re-run affected drivers with `QUANT_RESEARCH_OFFLINE=1` where appropriate, verify drift drops within tolerance
5. Only re-pin artifacts if changes are correct and necessary; document in ledger

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
