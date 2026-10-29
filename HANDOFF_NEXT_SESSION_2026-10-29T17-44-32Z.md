# Handoff — 2026-10-29T17:51:41Z

## Current State
- **Phase:** Research complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Baselines:** `experiments/*.json` are the authoritative golden artifacts, pinned by `ledger/golden_baseline.json`.
- **Verification:** Suite backs up/restores goldens; never leave a run half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
- **Data:** Cache coverage is enforced (`ledger/data_baseline.json`, `scripts/check_data_coverage.py`). E029 fundamentals and E030 panel are pinned.
- **Known issues:** E049 — optimizer determinism causes numeric drift in E041/E042 due to ill-conditioned QP (1-ulp sensitivity). Do **not** re-pin to silence; see ledger entry.

## Initial Task (Next Session)
1. **Verify baseline integrity** (required first)
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must pass: `check_goldens_clean`, `check_golden_baseline`, `tests/test_portfolio_opt.py`, and convention robustness.

2. **Assess health** (if `check.sh` passes)
   ```bash
   SEED=42 make verify-quick  # ~8 min
   ```
   Or `make verify` for convention-robustness only.

## Important Rules
- **Never** re-pin goldens as a side effect of running verification. Only re-pin via `scripts/check_golden_baseline.py --update` with explicit justification.
- **Never** commit verification outputs. If interrupted, restore goldens first.
- **Respect offline mode:** verification uses `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard.
- **Extended drift:** `--extended` reports drift in `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). E041 may still show numeric drift even after fixes — this is expected per E049.

## Suggested First Command
```bash
SEED=42 bash scripts/check.sh
```
