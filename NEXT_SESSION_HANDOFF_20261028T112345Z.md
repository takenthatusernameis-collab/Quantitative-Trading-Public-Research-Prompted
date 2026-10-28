# NEXT SESSION HANDOFF
Timestamp (UTC): 20261028T112345Z
Created by: current agentic session
Repo: Quantitative-Trading-Public-Research-Prompted

## Context
- Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical goldens live in `experiments/*.json`. The verification suite backs them up to `.verify_snapshot/`, re-runs drivers, and restores them afterward — never commit verification output.
- Baseline integrity is enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and `scripts/check_data_coverage.py` (all run by `make check`).
- Data: pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`; cache coverage pinned in `ledger/data_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer determinism: `src/portfolio_opt.py` validates on problem constraints (not solver status). Ill-conditioned QPs can still produce small numeric drift (see `AGENTS.md` and ledger E049). Do **not** re-pin goldens to silence drift.

## Clear initial task for next session
Start here in order:

1. **Verify baseline integrity**
   - Run: `SEED=42 make check` (fast). If it reports golden mismatch or stale snapshot, recover with `SEED=42 python3 run_all_verification.py --restore-only` before proceeding.
2. **Read the ledger**
   - Read `ledger/RESEARCH_LEDGER.md` top-to-bottom to understand surviving strategies, promotion gates, and open items (pay special attention to E041/E042 and the "do not re-pin" policy).
3. **Confirm reproducibility state**
   - If needed, run `SEED=42 make verify-quick` (~8 min). Extended/full are available if deeper verification is required.
4. **Decide next action**
   - Follow the ledger's stated disposition. If there is an explicit open item to address, tackle it; otherwise, do not run verification to "refresh" goldens and do not re-pin baselines. Only re-pin via `python3 scripts/check_golden_baseline.py --update` if you are intentionally changing a canonical artifact with justification recorded in the ledger.

## Quick references
- Commands: `AGENTS.md` (Quick Start, Reproducibility, Baseline Integrity)
- Verification: `run_all_verification.py` (flags: `--extended`, `--full`, `--skip-slow`, `--restore-only`)
- Guards: `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Artifacts: `experiments/*.json` (canonical), `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`
