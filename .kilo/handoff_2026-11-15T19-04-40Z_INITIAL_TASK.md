# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T19:04:40Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `c19be5ad` ("chore(kilo): checkpoint agent session")
**Sync:** `origin/main...HEAD` = `0 0` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. Handoff-refresh ledger entries run through E390. No open/pending/blocked research items recorded.
- **Working tree (non-handoff):** only compiled-bytecode/cache noise: `scripts/__pycache__/*.pyc`, `src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc` (see `git status --short`). No source, `experiments/*.json`, pinned `data/` input, or `ledger/` baseline file modified.
- **Verification snapshot:** `.verify_snapshot/` absent (no active/stale interrupted verification run detected at handoff time).
- **Goldens:** clean — `scripts/check_goldens_clean.py` (goldens match HEAD, exit 0) and `scripts/check_golden_baseline.py` (all 107 pinned goldens match `ledger/golden_baseline.json`, exit 0).
- **Data coverage:** clean — `scripts/check_data_coverage.py` reports all 35 pinned data inputs present, git-tracked and unchanged (exit 0). (This resolves the transient `data/panel.parquet` mismatch noted in the earlier 18:59:50Z handoff; no action needed.)
- **Convention robustness:** `verify_convention_robustness.py` → ALL VERIFICATIONS PASSED (exit 0).
- **Environment note:** Python deps/tools (numpy/pandas/scipy/pyarrow/statsmodels/yfinance/pytest, and `rg`) are NOT available in this sandbox; unit tests requiring them are not runnable here. Install per `requirements.txt` before running verification/tests.

### Per-step guard results (this session, no verification run)

- `scripts/check_json_artifacts.py` — 114 committed JSON artifacts parse → exit 0
- `scripts/check_goldens_clean.py` — committed goldens match HEAD → exit 0
- `scripts/check_golden_baseline.py` — 107 pinned goldens match baseline fingerprint → exit 0
- `scripts/check_data_coverage.py` — 35 pinned data inputs present/tracked/unchanged → exit 0
- `scripts/validate_template.py` — OK → exit 0
- `scripts/check_experiment_imports.py` — all drivers' calls/imports OK → exit 0
- `verify_convention_robustness.py` — all strategy blocks PASS → exit 0

## Delta vs prior durable handoff

- **Prior durable handoff:** `handoff_2026-11-15T19-03-00Z_INITIAL_TASK.md` (HEAD `82efa4c8` at that time).
- **Now:** HEAD advanced to `c19be5ad`; `git diff --name-only 82efa4c8..c19be5ad` filtered to research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, `ledger/`, excluding `__pycache__`/`*.pyc`) → **no paths**. No experiment, data, source, script, test, or ledger-baseline content changed. Only checkpoint commits and this handoff deliverable changed.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, change promotion gates/outcomes, re-run verification unprompted, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm clean research state; expect only `__pycache__`/handoff-artifact noise.
2. Confirm no interrupted verification run: `.verify_snapshot/` should be absent. If present or goldens look modified, recover first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md` — `git checkout <commit> -- experiments/<file>`). Never leave a verification run half-finished.
3. `pip install -r requirements.txt` if dependencies are missing.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`** (walk-forward + placebo RNG).
- Follow `AGENTS.md` scopes:
  - `make check` / `SEED=42 bash scripts/check.sh` (~seconds, offline)
  - `SEED=42 python3 verify_convention_robustness.py` (reads JSONs, no writes)
  - `SEED=42 python3 run_all_verification.py` (quick, ~8 min)
  - `SEED=42 python3 run_all_verification.py --extended` (~21 min)
  - `SEED=42 python3 run_all_verification.py --full` (~15 min)
- Verification overwrites and restores `experiments/*.json`; **never commit verification output** over goldens.
- Interrupted-run recovery: `SEED=42 python3 run_all_verification.py --restore-only`.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit verification output over canonical `experiments/*.json` goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional instruction and ledger justification.
- Do not reopen closed items: E049/E050 (optimizer determinism / exact KKT enumeration) or E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer must create via GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (research complete E001–E051; handoff refreshes through E390)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T19-04-40Z_INITIAL_TASK.md` (repo root), mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Supersedes operationally:** `handoff_2026-11-15T19-03-00Z_INITIAL_TASK.md` and earlier handoffs (retained for history).
- Generic handoff pointers repointed to this artifact via `scripts/repoint_handoff.py`.
- No experiments, data, source, tests, or ledger baselines modified for this handoff.