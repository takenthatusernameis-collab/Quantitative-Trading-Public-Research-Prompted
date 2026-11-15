# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T17:56:50Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `37a6cd48` ("chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** only `M src/__pycache__/cache_keys.cpython-312.pyc` (non-canonical `py_compile` artifact; no source, `experiments/*.json`, ledger, or data baseline changes).
- **Sync:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync with origin).
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Canonical artifacts/baselines:** `experiments/`, `data/`, `src/`, `scripts/`, `tests/` unchanged as research content; `ledger/golden_baseline.json` and `ledger/data_baseline.json` intact.
- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items. Handoff-refresh entries run through E386.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Delta vs prior durable handoff (`handoff_2026-11-15T17-55-20Z_INITIAL_TASK.md`, HEAD `333b0e9d` → `37a6cd48`):** `git diff --name-only 333b0e9d..37a6cd48` filtered to research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, excluding `__pycache__`/`*.pyc`) → **0 paths**. Only checkpoint commits, generic handoff pointer files, and `__pycache__/*.pyc` changed. No research substance changed.

## Baseline integrity (verified this session, per-step isolation; no verification run)

- `scripts/check_json_artifacts.py` → PASS (114 JSON artifacts parse)
- `scripts/check_goldens_clean.py` → PASS (goldens match HEAD)
- `scripts/check_golden_baseline.py` → PASS (all pinned goldens match)
- `scripts/check_data_coverage.py` → PASS (all pinned data inputs present/tracked/unchanged)
- `scripts/validate_template.py` → PASS
- `scripts/check_experiment_imports.py` → PASS
- `verify_convention_robustness.py` → PASS (all strategy blocks PASS)
- Unit tests are not runnable in this sandbox (`numpy` / `pandas` / `pytest` absent, unrelated to repo content). After `pip install -r requirements.txt` they run normally.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote state and note any uncommitted handoff/pointer or `__pycache__` noise.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (~seconds), `SEED=42 python3 verify_convention_robustness.py` (reads JSONs), `SEED=42 python3 run_all_verification.py` (quick ~8 min), `--extended` (~21 min), `--full` (~15 min).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (last research entry E051; handoff refreshes through E386)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T17-56-50Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-15T17-55-20Z_INITIAL_TASK.md` (HEAD `333b0e9d`) and earlier handoff artifacts (retained for history).
- This session created this handoff only; no code, experiments, ledgers, or baselines were modified.