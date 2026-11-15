# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T01:28:58Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `7428dd94` ("chore(kilo): checkpoint agent session"), in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (at handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items indicated beyond recorded closed items (e.g. E041/E042 ill-conditioned QP 1-ulp drift, E049/E050 closed — do not reopen).
- **Baseline integrity:** canonical artifacts are tracked `experiments/*.json` (107 tracked) plus pinned fingerprints in `ledger/golden_baseline.json` and `ledger/data_baseline.json`. **Confirmed this session:** `SEED=42 bash scripts/check.sh` → exit 0, "=== All checks passed ===" (py_compile, JSON artifacts parse, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment imports).
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` not present (no interrupted/pending verification observed).
- **Working tree:** only modified `__pycache__/*.pyc` files observed; no source, experiment, ledger, baseline, or data changes were made in this session. Do not commit `__pycache__` noise.
- **Delta vs prior durable handoff (E348, artifact `handoff_2026-11-15T01-24-49Z_INITIAL_TASK.md`, HEAD `3438fe0e` → `7428dd94`):** checkpoint commits only; `git diff --name-only 3438fe0e..7428dd94` filtered for research content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. No research substance changed.

## INITIAL TASK for next session

**Default: confirm baseline integrity, then await explicit user instructions.** Do not invent new experiments, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

1. **Confirm repo state**
   - `git status --short --branch` (expect clean aside from `__pycache__/*.pyc` noise; note any unexpected changes).
   - Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
2. **Environment & fast integrity checks** (before substantive work, if requested)
   - Install deps if needed: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
   - Run `SEED=42 bash scripts/check.sh` (or `make check`). Expect all checks to pass.
3. **If verification/reproduction is explicitly requested**
   - Always use **`SEED=42`**.
   - Scopes (`AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick), `--extended`, `--full`.
   - Verification overwrites then restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
4. **If asked to change research/code/baselines**
   - Follow pre-registration, baseline-integrity, and reproducibility rules in `AGENTS.md` and the ledger.
   - Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift; re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit verification output over canonical goldens (`experiments/*.json`).
- Never re-pin baselines without explicit, intentional instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys; never commit `__pycache__/*.pyc`.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T01:28:58Z_INITIAL_TASK.md` (repo root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`; generic canonical pointers (`LATEST*`, `NEXT*`, `INITIAL_TASK*`, `handoff_*`, etc.) repointed to this file.
- **Supersedes:** `handoff_2026-11-15T01-24-49Z_INITIAL_TASK.md` and prior handoffs as the current generic-pointer target.
- This session created/refreshed the durable handoff only; no source, experiment, ledger, baseline, or data artifacts were modified.