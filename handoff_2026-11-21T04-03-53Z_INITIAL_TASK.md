# Agent Handoff — Initial Task — 2026-11-21T04:03:53Z

## Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Branch**: `main` (HEAD cb537a92)
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Git state**: working tree clean; no active verification run; baseline ready.

## Key Commands
```bash
# Fast check (convention robustness + golden + baseline + data coverage + py_compile + tests)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min; 8 drivers in 5a block)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 committed drivers vs goldens)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes
- **Golden files**: `experiments/*.json` are canonical artifacts. Verification overwrites then restores them.
- **Never leave verification half-finished** — recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- **Seed**: Always `SEED=42` for walk-forward + placebo RNG reproducibility.
- **Data**: Cached parquet in `data/` (gitignored except pinned vintages). Offline enforced via `QUANT_RESEARCH_OFFLINE=1`.
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — maintainer-created via GitHub UI only.
- **Do not commit verification output**.

## Concrete Next Task (from HANDOFF_EXTENDED_VERIFICATION.md)
**Regenerate the stale E042_lead golden and add it to quick-mode verification.**

Evidence: `run_e042_lead.py` is deterministic across re-runs (excluding `timestamp`/`runtime_sec`); gate decisions unchanged (4/5 gates, REJECTED via G2 placebo z). Driver takes ~20s.

Steps:
1. Regenerate golden: `SEED=42 python3 experiments/run_e042_lead.py`
2. In `run_all_verification.py`, extend quick-mode `drivers` tuples with `expected_rc` and `exclude_keys`:
   - Add 6th element `expected_rc` (0 normally; `1` for E042_lead since REJECTED is expected).
   - Add 7th element `exclude_keys` (default `("timestamp",)`; `("timestamp","runtime_sec")` for E042_lead).
3. Update the comparison loop to use `expected_rc` instead of hard-coded `rc == 0` and pass `exclude_keys` to `compare_patterns`.
4. Add entry: `("experiments/run_e042_lead.py", "e042_lead_config_confirmatory.json", "run_e042_lead.py", [], None, 1, ("timestamp", "runtime_sec"))`.
5. Verify: `SEED=42 python3 run_all_verification.py` → ALL CHECKS PASSED.

Constraints: do not modify other committed goldens; preserve snapshot/restore; do not change E042_lead gate logic or pre-registered outcomes.

## First Action for Next Session
Run `SEED=42 bash scripts/check.sh` to confirm a clean baseline, then proceed to the E042_lead golden task above.
