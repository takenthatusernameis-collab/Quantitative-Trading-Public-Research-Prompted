# Handoff for Next Agentic Session
Timestamp (UTC): 2026-10-28T08-35-46Z
Repo: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
Branch/HEAD: (see git status)

## Current State
- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Active work: verification/safety guards and reproducibility (golden baseline protection, data cache coverage, extended verification drift tracking).
- Key open items in ledger: E049 (E041/E042 numeric drift from ill-conditioned tangency QP; optimizer determinism fixed but artifacts still drift beyond 1e-4) — do NOT re-pin to silence; accept/report per suite behavior.
- Verification must not overwrite committed goldens. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`. Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.

## Immediate Task
1. Read `AGENTS.md` fully for baseline integrity/reproducibility rules and verification commands.
2. Verify golden/data integrity before any changes: `SEED=42 bash scripts/check.sh` (should pass if clean).
3. If `check.sh` fails on golden/data guards, restore via `--restore-only` or checkout from correct HEAD; follow "Baseline Integrity" section strictly.
4. If clean, proceed to address any concrete task passed by user. If no specific task given, run a quick sanity check (e.g. `make verify-quick` with SEED=42) and report, without modifying `experiments/*.json` unless explicitly re-pinning under the documented procedure.

## Quick Commands
- Check: `SEED=42 bash scripts/check.sh` / `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` / `make verify-quick` (~8 min)
- Extended: `SEED=42 python3 run_all_verification.py --extended` / `make verify-extended` (~21 min)
- Full: `SEED=42 python3 run_all_verification.py --full` / `make verify-full`
- Restore only: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes
- Always use `SEED=42`.
- Do not re-pin goldens/data baselines as a side effect of verification.
- E029/E030 reproducibility relies on pinned snapshots (`data/fundamentals/`, `data/vintages.json`, `ledger/data_baseline.json`).
- Optimizer fix is in place (validate on problem constraints) per tests/test_portfolio_opt.py.
