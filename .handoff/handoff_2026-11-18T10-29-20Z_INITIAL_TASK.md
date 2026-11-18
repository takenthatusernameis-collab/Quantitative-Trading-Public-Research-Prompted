# Durable Handoff — Initial Task for Next Agentic Session

- **Handoff ID**: E491
- **Timestamp (UTC)**: 2026-11-18T10:29:20Z
- **HEAD**: `a7d8c96baf45db606338e96d6e71a1bf88f325ac` (`origin/main`, 0 ahead / 0 behind)
- **Prior handoff**: `handoff_2026-11-18T09-34-51Z_INITIAL_TASK.md` (E490)
- **Working tree at handoff creation**: clean (no tracked modifications, no `.verify_snapshot/ACTIVE.json`, no `.verify_reports/`)

## Repository state (closed research project)

- Research phase complete: E001–E051. Surviving/validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` are golden baselines pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`. Do **not** re-pin as a side effect of verification.
- Verification suite backs up/restores `experiments/` via repo-local `.verify_snapshot/` (gitignored). A run must never be left half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only` or restore pinned artifacts per `AGENTS.md`.
- CI workflow template is in `.github/workflow-templates/verification-gate.yml` (actual workflow cannot be created by agents here).

## Known open/monitoring items (see ledger)

- **E041 / E049**: E041 extended drift remains (133 numeric diffs, within 1-ulp sensitivity of ill-conditioned QP). Extended block still reports drift by design; **do not re-pin E041** to silence it. Optimizer determinism fix and constraints are documented in ledger E049 and enforced by `tests/test_portfolio_opt.py`.
- Extended drift reporting is informational (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, gitignored).

## Environment note (this runner)

- Observed at handoff time: `/usr/bin/python3` present, but core deps **not importable** (`pandas`, `numpy`, `scipy`, `pyarrow`, `statsmodels`, `yfinance` missing).
- Before running checks/verification, install deps: `python3 -m pip install -r requirements.txt` (and ensure optional solver deps only if needed; project falls back to `scipy.optimize`).

## Initial task for next session

1. **Confirm baseline integrity (no writes to goldens/data pins):**
   - `git status --short --branch` — expect clean or only intentional uncommitted work.
   - `git diff --name-only HEAD -- experiments/` — expect empty.
   - `SEED=42 bash scripts/check.sh` (fast, offline) once deps are installed.
2. **If a fuller reproduction is requested:** run `SEED=42 python3 run_all_verification.py` (quick) or `--extended`/`--full` per `AGENTS.md`. Ensure run completes so snapshot is restored; if interrupted, run `--restore-only` immediately and verify goldens match HEAD/pinned baseline before committing anything.
3. **If making changes:** follow pre-registration/ledger conventions in `AGENTS.md`; never commit `.verify_reports/`, `.verify_snapshot/`, or captured verification output; never commit `__pycache__`.
4. **Before ending session:** leave a new timestamped durable handoff (and mirror/repoint generic aliases via `python3 scripts/repoint_handoff.py <handoff_file>`), update `ledger/RESEARCH_LEDGER.md` if substantive work was done, and ensure `experiments/` remain clean vs HEAD/baseline.

## Constraints

- No new research goals were assigned in this session; treat repo as closed unless explicitly directed.
- Do not guess URLs, identities, or external state; use pinned data/artifacts and documented commands.
