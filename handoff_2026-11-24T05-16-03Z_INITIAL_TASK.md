# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T06:08:43Z
**Session ID**: Initial handoff created by user request
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

This is an independent reproducible quantitative-strategy research repository on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands Reference

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
# or
make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes (READ BEFORE RUNNING)

- `experiments/*.json` are canonical research artifacts. Verification suite overwrites them while re-running drivers and restores them afterwards — **never leave a verification run half-finished**
- Backup lives in repo-local, gitignored `.verify_snapshot/` with `ACTIVE.json` marker
- `scripts/check_goldens_clean.py` fails when tracked artifacts under `experiments/` differ from HEAD or when stale snapshot is pending
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
- If `scripts/check.sh` reports golden mismatch, fix it **before** committing
- `scripts/check_golden_baseline.py` compares every tracked artifact with SHA-256 fingerprint pinned in `ledger/golden_baseline.json`

## Current State

- All 43 experiments (E001–E043) completed
- Verified strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden baselines committed in `experiments/*.json`
- Data cached in `data/` (gitignored except pinned vintages)
- Dependencies: `pip install -r requirements.txt`

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Run `SEED=42 python3 run_all_verification.py --skip-slow` for quick convention check
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies
4. Any new experiments must follow pre-registration protocol with falsification expectations

---
*This handoff was created automatically at session start. Update as needed for continuity.*