# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T07:17:02Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `b8a9eee7` (`chore(kilo): checkpoint agent session`) — tracks `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)
- **Working tree:** not clean — 12 tracked `__pycache__/*.pyc` files modified (uncommitted bytecode drift only); **no source, experiment, ledger, test, or config edits** observed. Handle explicitly (restore/discard/commit only with explicit direction); do not let bytecode changes contaminate substantive commits.
  - `scripts/__pycache__/check_data_coverage.cpython-312.pyc`
  - `scripts/__pycache__/check_golden_baseline.cpython-312.pyc`
  - `scripts/__pycache__/check_goldens_clean.cpython-312.pyc`
  - `scripts/__pycache__/check_json_artifacts.cpython-312.pyc`
  - `scripts/__pycache__/diff_golden.cpython-312.pyc`
  - `src/__pycache__/data.cpython-312.pyc`
  - `tests/__pycache__/test_data_coverage.cpython-312.pyc`
  - `tests/__pycache__/test_drift_report.cpython-312.pyc`
  - `tests/__pycache__/test_golden_baseline.cpython-312.pyc`
  - `tests/__pycache__/test_goldens_guard.cpython-312.pyc`
  - `tests/__pycache__/test_json_guard.cpython-312.pyc`
  - `tests/__pycache__/test_portfolio_opt.cpython-312.pyc`
- **`.verify_snapshot/`:** absent (no interrupted verification run pending).
- **Golden guard:** `SEED=42 python3 scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (verified 2026-11-12T07:17:02Z).
- **Research phase:** complete (E001–E043). Authoritative dispositions/open items: `ledger/RESEARCH_LEDGER.md`.
- **Canonical baselines (authoritative):** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json` — do not modify or re-pin during routine verification.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)
**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**Before any substantive work (if requested):**
1. Run `git status --short --branch` and confirm HEAD/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted, recover first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`).
3. Treat tracked `__pycache__` modifications explicitly; do not mix bytecode-only changes into substantive commits without direction.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:**
- Always use `SEED=42`.
- Choose scope as directed: `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full`.
- **Never commit verification output** over `experiments/*.json`.
- If interrupted, restore goldens before committing (`--restore-only` or `git checkout -- experiments/` only when HEAD holds the pinned baseline).
- If guards report golden/baseline mismatch, fix/restore before committing — do not re-pin to silence drift.

## Reproduction / verification commands (run only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails
- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit or log secrets/keys.

## Handoff provenance
- **Durable artifact (this session):** `handoff_2026-11-12T07-17-02Z_INITIAL_TASK.md` (root).
- **Operational pointers:** root `handoff_*` convenience symlinks updated to target this artifact.
- **Supersedes operationally:** prior `handoff_*_INITIAL_TASK.md` artifacts/symlinks (retained for history).
