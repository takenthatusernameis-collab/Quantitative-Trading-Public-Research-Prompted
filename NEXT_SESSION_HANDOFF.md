# Durable Handoff — Next Agentic Work Session

**Created:** 2026-10-29T07:06:43Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Git repo present | Research phase complete (E001–E043)

## Initial Task (Start Here)

**Objective:** Maintain baseline integrity and continue from the committed research state. Do not re-run experiments to "refresh" goldens or silently modify canonical artifacts.

### Priority 1: Verify Baseline Integrity
Before making any changes:
```bash
SEED=42 bash scripts/check.sh
```
Confirm: no golden mismatches, no stale `.verify_snapshot/ACTIVE.json`, data coverage passes, and tests pass. If interrupted from a previous verification run, recover first:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```

### Priority 2: Understand Current Disposition
Read these first to understand constraints and known open items:
- `AGENTS.md` — verification commands, golden protection rules, cache/data invariants
- `ledger/RESEARCH_LEDGER.md` — validated strategies and open items (notably E041 numeric drift from ill-conditioned QP; do not re-pin)
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` — pinned fingerprints

### Priority 3: Work Only On Explicit Requests
- **Goldens are authoritative.** Never modify `experiments/*.json` as a side effect of verification. Changes require explicit re-pinning via `scripts/check_golden_baseline.py --update` with justification.
- **Data inputs.** If adding data, commit the file and re-pin via `scripts/check_data_coverage.py --update`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- **Verification.** Use `make check`/`make verify-quick`/`make verify-extended`/`make verify-full` as needed. Extended drift is reported to gitignored `.verify_reports/` only.

## Quick Reference
```bash
# Fast integrity check
SEED=42 bash scripts/check.sh

# Quick/full verification (restores goldens after)
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Recover if left half-finished
SEED=42 python3 run_all_verification.py --restore-only
```
