# Agentic Work Session Handoff

**Created:** 2026-11-25T01:17:40Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Git repo: yes. Working tree clean (no uncommitted changes at handoff time).
- Verification suite is active-state sensitive: `experiments/*.json` are canonical artifacts, backed up/restored by `run_all_verification.py`. Never leave a verification run half-finished; never commit verification output.
- Cache coverage invariant enforced by `scripts/check_data_coverage.py` (cache files git-tracked + SHA-256 pinned in `ledger/data_baseline.json`). Drivers run with `QUANT_RESEARCH_OFFLINE=1`.
- `cvxpy`/`cvxopt` optional; `src/portfolio_opt.py` falls back to `scipy.optimize`.

## Recommended first task for next session

Run the convention-robustness check + template validation (fast, offline, seconds):

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If green, proceed to quick full verification:

```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

## Key commands reference

| Task | Command |
|------|---------|
| Fast check + template validation | `SEED=42 bash scripts/check.sh` |
| Quick full verification (~8 min) | `SEED=42 python3 run_all_verification.py` |
| Extended verification (~21 min) | `SEED=42 python3 run_all_verification.py --extended` |
| Full verification (~15 min, n_sim=50) | `SEED=42 python3 run_all_verification.py --full` |
| Skip slow batch/regression steps | `SEED=42 python3 run_all_verification.py --skip-slow` |
| Restore golden artifacts after interruption | `SEED=42 python3 run_all_verification.py --restore-only` |
| Recover baseline from HEAD | `git checkout -- experiments/` |
| Compile check on changed Python files | `python3 -m py_compile <file>` |

## Constraints to honor

- Always run with `SEED=42`.
- Do not commit verification output or half-finished run artifacts.
- Re-pinning a golden requires `python3 scripts/check_golden_baseline.py --update` and a ledger entry (E050 precedent).
- Adding a data input: commit the file, then `python3 scripts/check_data_coverage.py --update`.
- CI gate workflow cannot be auto-created by agents; template at `.github/workflow-templates/verification-gate.yml`.

## Open questions / blockers

None at handoff time.
