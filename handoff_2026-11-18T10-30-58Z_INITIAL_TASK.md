# Durable Handoff — Initial Task for Next Agentic Session

- **Handoff ID**: E492
- **Timestamp (UTC)**: 2026-11-18T10:30:58Z
- **HEAD**: `main` (tracked `origin/main`), working tree clean at handoff creation
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Prior handoff**: `handoff_2026-11-18T10-29-20Z_INITIAL_TASK.md` (E491)

## Repository state (closed research project)

- Research phase complete: E001–E051. Surviving/validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` are golden baselines pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`. Do **not** re-pin as a side effect of verification.
- Verification suite backs up/restores `experiments/` via repo-local `.verify_snapshot/` (gitignored). A run must never be left half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only` or restore pinned artifacts per `AGENTS.md`.
- CI workflow template is in `.github/workflow-templates/verification-gate.yml` (actual workflow cannot be created by agents here).

## Known open/monitoring items (see ledger)

- **E041 / E049**: E041 extended drift remains (133 numeric diffs, within 1-ulp sensitivity of ill-conditioned QP). Extended block still reports drift by design; **do not re-pin E041** to silence it. Optimizer determinism fix and constraints are documented in ledger E049 and enforced by `tests/test_portfolio_opt.py`.
- Extended drift reporting is informational (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, gitignored).

## Environment note (this runner)

- `/usr/bin/python3` present, but core deps **not importable** (`pandas`, `numpy`, `scipy`, `pyarrow`, `statsmodels`, `yfinance` missing) unless installed.
- Before running checks/verification, install deps: `python3 -m pip install -r requirements.txt`.

## Initial task for next session

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

Before any substantive work (if requested):

1. `git status --short --branch` — confirm HEAD/remote alignment and note uncommitted files.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

If verification / reproduction is explicitly requested:

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (last research entry E051)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-18T10-30-58Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.
