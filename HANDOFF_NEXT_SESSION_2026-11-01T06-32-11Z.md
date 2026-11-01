# Handoff — 2026-11-01T06:32:11Z

## Initial task for next session
Start from a clean, verified baseline: run `SEED=42 bash scripts/check.sh` and address any golden/data mismatch first. Then review open items in `ledger/RESEARCH_LEDGER.md` (notably E041 optimizer determinism) and pick the highest-priority open item to close with a pre-registered analysis/driver or document promotion/rejection evidence.

## Current state
- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` canonical goldens; pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- **Known notes:** E029/E030 reproduce offline; E041 has 1-ulp optimizer sensitivity (133 numeric diffs) — do not re-pin to silence.
- **Recovery:** `.verify_snapshot/ACTIVE.json`; `SEED=42 python3 run_all_verification.py --restore-only`.

## Immediate priorities
1. `SEED=42 bash scripts/check.sh` (or `make check`).
2. Review open items in ledger.
3. `git status --short` — restore if verification left artifacts.

## Quick references
- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 experiments/run_e0XX.py ...`
