# HANDOFF — 2026-11-01T16:18:38Z (UTC)

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch: main
- HEAD: d9ecac7 chore(kilo): checkpoint agent session
- Working tree: clean (0 modified files)
- Platform: Linux
- Goal: Independent reproducible quantitative research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

## Current State
- Golden baselines are authoritative (`experiments/*.json`, pinned in `ledger/golden_baseline.json`).
- Verification suite exists with backup/recovery via `.verify_snapshot/` (gitignored). Never leave a verification run half-finished.
- Data coverage enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`. Missing/pinned caches required; offline mode used by verification.
- Optimizer determinism fixed (E049) but E041/E042 grid still show small numeric drift due to ill-conditioned QP (not to be re-pinned).

## Immediate Priorities for Next Session
1. **Verify baseline integrity first** (before any changes):
   ```bash
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```
   If any fail, restore per AGENTS.md before proceeding.

2. **Run quick verification** to confirm environment is healthy:
   ```bash
   SEED=42 python3 run_all_verification.py  # or make verify-quick
   ```
   Expect ~8 min. Do not interrupt; if interrupted, recover with `--restore-only`.

3. **Address open items from ledger** (check `ledger/RESEARCH_LEDGER.md` for current open/follow-ups). Key known items:
   - E041 numeric drift (133 diffs) from QP conditioning — root-caused, fixed in optimizer validation but artifact still drifts; do **not** re-pin to silence.
   - E042 sensitivity grid similar conditioning issue.
   - Ensure any new data inputs are committed and re-pinned via `check_data_coverage.py --update`.

## Safe Workflow Rules
- Always use `SEED=42` for walk-forward/placebo.
- Never modify `experiments/*.json` as a side effect of verification — restore after runs.
- If you need to replace a golden, update via `scripts/check_golden_baseline.py --update` (and justify in commit/ledger).
- Run `python3 -m py_compile` on changed Python files. Linting not separately configured.
- Do not commit verification artifacts/output.
- Follow pre-registration: gates/falsification must not be moved post-hoc.

## Quick Commands Reference
```bash
# Checks
SEED=42 bash scripts/check.sh        # fast checks + validation
make check

# Verification
SEED=42 python3 run_all_verification.py           # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only

# Individual
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## Handoff Notes
- Research is complete; focus should be on reproducibility/integrity, ledger maintenance, or addressing any new issues found.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`); use template in `.github/workflow-templates/verification-gate.yml` if needed.
- Data vintages: `data/vintages.json` (2026-10-12 pinned), 2026-10-11 committed for specific experiments; fundamentals pinned separately.
- If you see golden mismatches, **fix before committing**. Check HEAD vs baseline carefully.

**Initial task for next session:** Verify baseline integrity (goldens, data coverage, baseline ledger) and run quick verification to confirm green state. Report any drift/mismatches and do not re-pin artifacts without explicit justification and ledger update.
