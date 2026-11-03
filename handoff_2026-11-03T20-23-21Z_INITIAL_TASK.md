# HANDOFF - Next Agentic Session
**Timestamp:** 2026-11-03T21:15:55Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** see `git log -1 --oneline`

## Current State
- **Research phase:** Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are committed goldens. `ledger/golden_baseline.json` and `ledger/data_baseline.json` pin their integrity.
- **Verification:** `run_all_verification.py` backs up/restores goldens. Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- **Data:** Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Verification runs offline via `QUANT_RESEARCH_OFFLINE=1`.
- **Known drift:** E041/E042 can show numeric drift (ill-conditioned QP, optimizer status handling fixed per E049) — do **not** re-pin to silence.

## Initial Task (clear, actionable)
1. **Verify integrity first** (required before any changes):
   ```bash
   SEED=42 make check
   ```
   If it fails due to a pending snapshot, recover: `SEED=42 python3 run_all_verification.py --restore-only` and re-run check.
2. **Read context**:
   - `ledger/RESEARCH_LEDGER.md` (open items, promotion gates, falsification)
   - `AGENTS.md` (commands, guards, conventions)
   - `ledger/golden_baseline.json`, `ledger/data_baseline.json`
3. **Ask user for priority** after confirming green. Do not modify `experiments/` goldens as a side effect of verification. If adding data, commit files and update baselines via the provided scripts.

## Quick Commands
```bash
SEED=42 make check        # fast guards + template validation
SEED=42 make verify-quick # ~8 min
SEED=42 make verify-extended
SEED=42 make verify-full
```

## Notes
- Never start verification if `scripts/check_goldens_clean.py` reports a stale snapshot owned by another PID.
- Re-pinning goldens requires explicit `--update` and should only happen with justification recorded in the ledger.
- If interrupted mid-verification, always restore before committing.
