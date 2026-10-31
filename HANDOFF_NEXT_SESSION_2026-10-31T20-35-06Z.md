# HANDOFF — 2026-10-31T20:35:06Z

## Current state
- Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Git repo: yes (HEAD is the current checkpoint).

## Initial task for next session
1. **Verify baseline integrity (blocking)**
   - Run: `SEED=42 bash scripts/check.sh` (or `make check`)
   - Ensure `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass. If there is a stale snapshot, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
2. **Confirm reproducibility (quick)**
   - Run: `SEED=42 python3 run_all_verification.py` (quick, ~8 min) or `make verify-quick`
   - Do not commit verification outputs. If interrupted, restore before committing.
3. **Pick next concrete work**
   - Review `ledger/RESEARCH_LEDGER.md` for open items (notably E041 optimizer/ill-conditioned QP drift, cache coverage enforcement, and any remaining follow-ups). Choose a single scoped task and proceed from there.

## Key constraints / gotchas
- Always use `SEED=42`.
- Verification overwrites `experiments/*.json` temporarily and restores; never leave a run half-finished.
- Do not re-pin goldens to silence expected numeric drift (e.g. E041/E042 grid). Only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit justification.
- E029 fundamentals and E030 panel are pinned (offline-reproducible). Other inputs must satisfy `scripts/check_data_coverage.py` (re-pin with `--update` when adding data).
- Portfolio optimizer validates on constraints (not solver exit status) per `tests/test_portfolio_opt.py`.

## References
- `AGENTS.md` — commands, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — decisions, gates, open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `run_all_verification.py`, `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`
(End of file)