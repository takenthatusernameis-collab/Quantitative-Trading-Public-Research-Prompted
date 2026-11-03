# INITIAL TASK - 2026-11-03T19:25:01Z

## Session Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch: main
- HEAD: 452ded4 (chore(kilo): checkpoint agent session)
- Working tree clean
- Generated: 2026-11-03T19:25:01Z

## Project State
Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. All experiments are pre-registered with falsification gates. The committed golden artifacts under `experiments/` are canonical and pinned via `ledger/golden_baseline.json`.

## Handoff Notes
- Verification suite will overwrite `experiments/*.json` during runs and restores them afterwards. Never leave a verification run half-finished.
- Stale snapshots live in gitignored `.verify_snapshot/` with `ACTIVE.json` (pid) if interrupted; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- `scripts/check.sh` runs `check_goldens_clean.py`, `check_golden_baseline.py`, and `check_data_coverage.py`. All must pass before committing.
- Do **not** re-pin goldens as a side effect of verification. To update a pinned baseline, use `scripts/check_golden_baseline.py --update` (and/or `scripts/check_data_coverage.py --update`) with justification.
- Known sensitivities: portfolio optimizer (E041/E042) has 1-ulp sensitivity; see AGENTS.md and `ledger/RESEARCH_LEDGER.md` (E049).
- Data coverage is enforced offline during verification (`QUANT_RESEARCH_OFFLINE=1`).

## Priority Tasks
1. **Preserve baseline integrity** - Before any commit touching experiments/goldens or verification, run `SEED=42 bash scripts/check.sh`. If it reports a golden mismatch and working tree is dirty from an interrupted run, restore first.
2. **Follow conventions strictly** - Always use `SEED=42`. Respect pre-registration, goalposts, and multiple-testing discipline. Never commit verification output artifacts.
3. **Handle interruptions safely** - If a previous verification was killed mid-run, recover via `--restore-only` (or `git checkout -- experiments/`) before starting new work.
4. **When adding data** - Commit the data file and re-pin via `scripts/check_data_coverage.py --update`; verification will run offline.

## Quick Commands
```bash
# Fast check (goldens clean + baseline + data coverage + py_compile + tests)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended/full if needed
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Recovery
SEED=42 python3 run_all_verification.py --restore-only
```

## References
- `AGENTS.md` - Full conventions, gotchas, verification details
- `ledger/RESEARCH_LEDGER.md` - Experiment history and decisions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` - Pinned baselines
