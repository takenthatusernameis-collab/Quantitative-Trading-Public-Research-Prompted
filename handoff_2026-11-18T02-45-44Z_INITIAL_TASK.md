# Durable handoff — agentic work session

## Timestamp
2026-11-18T02:46:29Z

## Current state
- Repository: Quantitative-Trading-Public-Research-Prompted
- Branch/working tree: clean assumption unless git status says otherwise
- Research phase complete (E001–E043); validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Canonical research artifacts: `experiments/*.json` — must not be modified by verification runs
- Verification commands (from AGENTS.md):
  - Fast: `SEED=42 bash scripts/check.sh` (or `make check`)
  - Quick full (~8 min): `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
  - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (or `make verify-extended`)
  - Full (~15 min): `SEED=42 python3 run_all_verification.py --full` (or `make verify-full`)
  - Skip slow: `SEED=42 python3 run_all_verification.py --skip-slow`
  - Restore goldens after interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`

## Next task
Continue / run the verification suite and keep `experiments/*.json` baseline clean. Do not commit verification output as a side effect. If a run is interrupted, restore with `--restore-only` (or `git checkout -- experiments/`). Any replacement of a committed golden requires re-pinning via `python3 scripts/check_golden_baseline.py --update` and putting the change in the diff.

## Open items (from AGENTS.md / ledger)
- E041 (min-var confirmatory): still reports ~133 numeric drift differences (1-ulp QP sensitivity); do not re-pin to silence. See ledger E049/E041 entry.
- CI verification-gate workflow cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml` must be created by a maintainer via GitHub UI.

## Constraints
- Always use `SEED=42`
- Run `QUANT_RESEARCH_OFFLINE=1` for verification (missing cache fails hard)
- Data/cache additions must be committed and re-pinned via `python3 scripts/check_data_coverage.py --update`
- No separate linter configured; run `python3 -m py_compile` on changed Python files
- Do not add comments to code unless asked
