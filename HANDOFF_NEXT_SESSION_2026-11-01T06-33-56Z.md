# Handoff — 2026-11-01T06:33:56Z

## Initial task for next session

Establish a clean, verified baseline before any new research work:

1. `SEED=42 bash scripts/check.sh` (or `make check`) — runs `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `py_compile`, and `test_portfolio_opt.py`. Expected: EXIT 0 with "=== All checks passed ===".
2. `git status --short` — confirm the working tree is clean (no stray `experiments/*.json` or `.verify_snapshot/` artifacts). If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
3. Only after steps 1–2 pass cleanly, review `ledger/RESEARCH_LEDGER.md` open items and pick the highest-priority open item to close with a pre-registered analysis/driver or document promotion/rejection evidence.

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- **Known notes:** E029/E030 reproduce offline; E041 has 1-ulp optimizer sensitivity (133 numeric diffs on ill-conditioned QP) — do **not** re-pin to silence (ledger E049 open item).
- **Recovery:** `.verify_snapshot/ACTIVE.json`; `SEED=42 python3 run_all_verification.py --restore-only`.
- **Git:** working tree clean (no non-`__pycache__` modifications as of this handoff).

## Immediate priorities

1. `SEED=42 bash scripts/check.sh` (or `make check`).
2. `git status --short` — restore if verification left artifacts.
3. Review open items in `ledger/RESEARCH_LEDGER.md` (notably E041 optimizer determinism / E042 grid drift).
4. Execute the highest-priority open item with a pre-registered plan; record result in the ledger.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 experiments/run_e0XX.py ...`
- `QUANT_RESEARCH_OFFLINE=1` for offline driver runs.