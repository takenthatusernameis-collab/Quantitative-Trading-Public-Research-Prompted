# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T11:35:41Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes for Next Session

- **Golden artifacts**: `experiments/*.json` are canonical baselines. Verification overwrites and restores them — never leave a run half-finished.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Cache coverage is enforced invariant.
- **Reproducibility**: Always use `SEED=42`. Close-to-close is v1.2.3 primary convention.
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — maintainer must create via GitHub UI.

## Current Baseline Integrity

Run `scripts/check.sh` before any work to verify golden artifacts match HEAD and no stale snapshot is pending.

---

*This handoff was created automatically at session start. Update as needed during work.*