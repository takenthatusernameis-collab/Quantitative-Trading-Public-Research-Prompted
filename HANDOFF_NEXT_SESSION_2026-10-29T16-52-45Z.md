# Handoff for Next Agentic Work Session

**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md. Current HEAD: 6c1768f (chore(kilo): checkpoint agent session).

## Current State Summary

- **Research status:** Phase complete. Validated/partial results in `ledger/RESEARCH_LEDGER.md`.
- **Verification state:** Canonical artifacts in `experiments/*.json` are tracked. Verification suite backs up/restores them. Do not leave verification runs half-finished.
- **Data:** Cached data in `data/` (some gitignored). Pinned vintages in `data/vintages.json` and fundamentals in `data/fundamentals/`. Cache coverage enforced by `scripts/check_data_coverage.py`.
- **Baseline integrity:** Guards in place (`check_goldens_clean.py`, `check_golden_baseline.py`). Never re-pin baselines as side effect of verification.

## Immediate Next Task (Clear Initial Task Message)

**Task:** Continue from the most recent validated state with verification integrity intact.

### Objectives
1. **Verify baseline integrity** before making changes
   - Run `SEED=42 bash scripts/check.sh` to confirm goldens clean, data coverage OK, py_compile OK.
   - If it reports issues, restore: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate.

2. **Understand current validated strategies** (quick orientation)
   - Read `ledger/RESEARCH_LEDGER.md` top entries for surviving strategies (market-neutral keeper, blends).
   - Note conventions: close-to-close v1.2.3 primary, overnight decomposition reported, costs tc=0.5bps + slippage=0.2bps, next-day open execution.

3. **Pick highest-value next research action** based on ledger gaps
   - Check for any open items/TODOs in ledger (e.g. E041 optimizer determinism numeric drift noted as open).
   - Common next directions from prior handoffs: optimize TSM+DN blend weights, test third component for diversification, or address any concrete open items.
   - If unclear, propose 1-2 concrete hypotheses with falsification criteria before implementing.

### Constraints & Rules
- Always use `SEED=42` for reproducibility.
- Do not modify `experiments/*.json` golden files. Verification restores them.
- Follow pre-registration discipline; don't move goalposts post-hoc.
- Run `SEED=42 bash scripts/check.sh` before committing.
- Costs/execution conventions as above.
- If adding data inputs, commit files and re-pin via `scripts/check_data_coverage.py --update`.

### Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --quick  # or --extended/--full as needed
SEED=42 python3 run_all_verification.py --restore-only
```

### Files to read first
- `ledger/RESEARCH_LEDGER.md` (authoritative results)
- `AGENTS.md` (commands/conventions)
- `src/strategies.py`, `src/backtest.py`, `src/validate.py` (understand interfaces)
