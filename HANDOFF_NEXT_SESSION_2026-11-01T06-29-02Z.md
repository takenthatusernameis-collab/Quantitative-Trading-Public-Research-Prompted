# Handoff — 2026-11-01T06:31:26Z

## Current state
- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are canonical goldens. `ledger/golden_baseline.json` and `ledger/data_baseline.json` pin fingerprints; changes require explicit re-pinning.
- **Verification guards active:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` (enforced).
- **Known reproducibility notes:** E029 fundamentals and E030 panel are pinned; E029/E030 reproduce offline. E041 has known 1-ulp optimizer sensitivity (133 numeric diffs remain) — do **not** re-pin to silence.
- **Recovery:** `.verify_snapshot/` with `ACTIVE.json` tracks live runs. Use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` if interrupted.

## Immediate priorities (do first)
1. **Verify baseline integrity**
   `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/data mismatch before making changes.
2. **Review open items**
   Read `ledger/RESEARCH_LEDGER.md` for open/follow-up items (notably E041 optimizer determinism and any promotion gates).
3. **Confirm clean tree**
   `git status --short` — if verification left artifacts modified, restore before committing.

## Suggested next task
Pick the highest-priority open item from the ledger and either (a) close it with a pre-registered analysis/driver, or (b) document evidence for promotion/rejection. Follow pre-registration, multiple-testing discipline, and the "goldens are authoritative" rule. If you need to re-run verification, use the snapshot-safe flow and never commit verification output.

## Quick references
- Fast checks: `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Individual: `SEED=42 python3 experiments/run_e0XX.py ...`
- Data: cached in `data/` (gitignored except pinned vintages/fundamentals); `QUANT_RESEARCH_OFFLINE=1` enforced by suite
