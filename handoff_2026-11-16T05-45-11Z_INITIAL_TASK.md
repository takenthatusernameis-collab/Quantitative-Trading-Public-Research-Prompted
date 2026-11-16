# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T05:45:11Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task for Next Session

1. Run `make check` (or `SEED=42 bash scripts/check.sh`) to verify baseline integrity before any new work.
2. Confirm `experiments/*.json` golden files match `HEAD` / `ledger/golden_baseline.json`; if a mismatch is reported, fix it before committing — never commit verification output.
3. If the verification suite was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Continue from the known-good state in `AGENTS.md`; seed must always be `SEED=42`.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands

```bash
# Fast convention-robustness check (~seconds, offline)
SEED=42 bash scripts/check.sh
# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Key Files

- `ledger/RESEARCH_LEDGER.md` — validated strategies (E041 optimizer determinism drift, E029/E030 pinned data status open items)
- `experiments/*.json` — canonical research artifacts (golden files; never commit verification output)
- `scripts/check.sh` — convention robustness check
- `run_all_verification.py` — full verification suite
- `AGENTS.md` — project commands & conventions

## Important Notes

- Golden files in `experiments/` are committed artifacts — the verification suite overwrites and restores them; a half-finished run must never be left uncommitted.
- Data cached in `data/` (gitignored except pinned vintages); cache coverage is enforced via `scripts/check_data_coverage.py`.
- Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
