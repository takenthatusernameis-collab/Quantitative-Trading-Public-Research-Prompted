# DURABLE HANDOFF
**Timestamp:** 2026-11-02T09:38:55Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working Dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State
- **Research phase:** Complete (E001–E043). Validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are committed goldens. The verification suite backs up and restores them — they must never be overwritten without explicit re-pinning.
- **Baseline guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and `scripts/check_data_coverage.py` are enforced (see `AGENTS.md` Baseline Integrity).
- **Known open item:** E041 numeric drift persists due to an ill-conditioned QP (optimizer fix applied). 133 numeric diffs remain; do **not** re-pin to silence. See `ledger/RESEARCH_LEDGER.md` for details.

## Immediate Task for Next Agent
1. **Run integrity check** - Execute `SEED=42 bash scripts/check.sh` (or `make check`). All steps must pass.
2. **Recover if interrupted** - If goldens are dirty from a previous run, restore first: `SEED=42 python3 run_all_verification.py --restore-only`, then re-run the check.
3. **Report status** - Summarize pass/fail of the check, confirm canonical goldens are intact, and note any open ledger items. Do not start new experiments or re-run verification unless explicitly requested.

## Critical Constraints
- **Always use `SEED=42`** for any reproduction runs.
- **Never commit verification output** that overwrites canonical artifacts.
- **Respect baseline integrity** - Re-pinning requires explicit justification and use of `--update` flags; never as a side effect of verification.
- **Offline-first** - Verification runs with `QUANT_RESEARCH_OFFLINE=1`. Missing cached data must be committed and re-pinned via `scripts/check_data_coverage.py --update`.

## Key References
- `AGENTS.md` - Commands, conventions, and baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` - Research history and open items
- `ledger/golden_baseline.json` - Pinned SHA-256s for experiment artifacts
- `ledger/data_baseline.json` - Pinned SHA-256s for cached data inputs
- `run_all_verification.py` - Verification suite with backup/restore