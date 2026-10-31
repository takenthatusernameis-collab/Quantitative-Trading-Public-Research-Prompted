# HANDOFF - 2026-10-31T02:06:44Z

## Current State
- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are committed goldens. `ledger/golden_baseline.json` and `ledger/data_baseline.json` pin their SHA-256 fingerprints.
- **Data:** Cached in `data/` (gitignored except pinned vintages). Fundamentals pinned in `data/fundamentals/`. Cache coverage is enforced.
- **Verification:** `run_all_verification.py` backs up/restores goldens; never modify them as a side effect of a run.

## Immediate Next Task
**Verify repository integrity before making any changes.**

```bash
SEED=42 bash scripts/check.sh
```

If it passes cleanly, proceed to review open items in the ledger. If it fails due to golden drift or a stale snapshot:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or git checkout -- experiments/
```
Do not re-pin goldens to silence failures - follow `AGENTS.md` baseline integrity rules.

## Open Items To Be Aware Of
- **E041 numeric drift (optimizer determinism):** 354 → 133 numeric diffs remain after fixing SLSQP status gating. Ill-conditioned QP causes 1-ulp sensitivity; do **not** re-pin. See `ledger/RESEARCH_LEDGER.md` E049.
- **E042/E041 grid sensitivity:** Some artifacts remain numerically sensitive; treat as reporting drift, not regression.
- **Extended verification:** `make verify-extended` reports drift in `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).

## Key References
- `AGENTS.md` — commands, conventions, baseline integrity (critical)
- `ledger/RESEARCH_LEDGER.md` — results, gates, open items
- `run_all_verification.py` — quick/extended/full verification
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Conventions
- Always use `SEED=42`
- Close-to-close v1.2.3 primary; overnight decomposition reported
- Multiple-testing: grids reported, not gated; confirmatory runs need placebo
- Never commit verification output if interrupted - restore first
- Offline reproducibility enforced (`QUANT_RESEARCH_OFFLINE=1` during verification)
