# HANDOFF — Next Agentic Work Session (2026-10-27T23:34:54Z)

## Current State
- Repo is clean at HEAD b2e49c4 (chore(kilo): checkpoint agent session). Latest work was session checkpoints.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts in `experiments/*.json` are the goldens. Verification suite backs up/restores them (`.verify_snapshot/`, `ACTIVE.json`).
- Guards in place: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`. All must pass before commit.
- Data coverage enforced (all `data.download()` sites pinned in `ledger/data_baseline.json`); verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Known Open Items (from ledger/AGENTS.md)
- **E041 (optimizer determinism)**: 354 numeric diffs reduced to 133 after fixing optimizer validation (status 8 allowed if feasible/optimal). 133 remain due to 1-ulp sensitivity of ill-conditioned QP; 3 structural differences gone. Still exceeds 1e-4 tolerance — do **not** re-pin to silence. See `ledger/RESEARCH_LEDGER.md` E049.
- **E042 lead**: related optimizer sensitivity; gate logic fixed (constraint-validation, not solver status). Artifacts may drift slightly in extended verification.
- **E029/E030**: made offline-reproducible by pinning fundamentals/panel; goldens re-pinned deliberately. Do not "fix" by re-running to change them.
- **CI workflow**: cannot be created by agents (controller restores `.github/workflows/`, token lacks `workflows` scope). Template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.

## Recommended First Actions
1. **Verify repo hygiene** (fast, offline):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs py_compile, tests (incl. `tests/test_portfolio_opt.py`), `check_goldens_clean.py`, `check_golden_baseline.py`, `verify_convention_robustness.py`, template validation.
2. **Quick full verification** (if you need confidence in drivers):
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Backs up/restores goldens. Never leave interrupted; recover with `--restore-only` if needed.
3. **Check for pending snapshot**: if `scripts/check_goldens_clean.py` warns about stale snapshot, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

## Suggested Next Work (pick one)
- **Triage E041 drift**: Investigate remaining 133 numeric diffs in E041 extended block. Understand if they can be reduced (better scaling/conditioning, more stable solver settings) without changing optimization logic inappropriately. Do not re-pin goldens. Document findings in ledger if changes made.
- **Harden verification**: Review extended drift reporting (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`) — deterministic, gitignored. Consider if tolerances need adjustment or if specific cases need explicit handling, but only if justified and pre-registered.
- **Data coverage audit**: Run `python3 scripts/check_data_coverage.py` to confirm all cached inputs match pins. If adding new data, commit file and update pins with `--update`.
- **Docs/ledger**: Update `ledger/RESEARCH_LEDGER.md` with any findings from above, keeping pre-registration/falsification discipline.

## Key References
- `AGENTS.md` — full commands, conventions, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — experiment outcomes, E041/E042/E048/E049 details
- `run_all_verification.py`, `scripts/check.sh`, `verify_convention_robustness.py`
- `src/portfolio_opt.py`, `tests/test_portfolio_opt.py` — optimizer determinism
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Notes
- Always use `SEED=42`.
- Verification overwrites `experiments/*.json` temporarily — never commit in middle of run.
- If goldens appear modified unexpectedly, restore from HEAD or use `--restore-only`. If HEAD already has a bad commit, restore from last good commit matching `ledger/golden_baseline.json`.
