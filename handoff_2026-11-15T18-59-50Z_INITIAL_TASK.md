# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T18:59:50Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `01561ca7` ("chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree (non-handoff):** `M src/__pycache__/cache_keys.cpython-312.pyc` only (compiled artifact; no source, `experiments/*.json`, ledger-baseline, or pinned-data changes).
- **Sync:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (in sync with `origin/main`).
- **Interrupted verification:** `scripts/check.sh` reports a **live verification run** (pid 58418) temporarily modifying goldens, plus a **stale snapshot** (pid 999999, no longer running) in the temp workspace. The committed goldens in `experiments/` may be overwritten. **Recovery required before substantive work**: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- **Data coverage issue:** `scripts/check_data_coverage.py` reports `data/panel.parquet` fingerprint mismatch (pinned: `320e00e7...` vs actual: `9d6f965a...`), not git-tracked, and manifest unreadable in the temp workspace. This file is a dynamic-only request; the pinned baseline expects the committed snapshot. If a driver needs this input it will re-download from network.
- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items. Handoff-refresh ledger entries through E390.
- **Closed — do not reopen:** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Delta vs prior durable handoff (`handoff_2026-11-15T18-56-32Z_INITIAL_TASK.md`, HEAD `40009b74`)

- `git diff --name-only 40009b74..01561ca7` filtered to research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, `ledger/`, excluding `__pycache__`/`*.pyc`) → **0 paths** (no research content changed).
- Only checkpoint commit and this handoff deliverable changed. **No research substance changed.**

## Baseline integrity (partial — blocked by live verification run)

Repo-level guard steps that ran clean (exit 0):
- `scripts/check_json_artifacts.py` (114 JSON artifacts parse)
- `scripts/check_goldens_clean.py` — **FAIL**: live verification run detected (goldens temporarily modified); recovery needed
- `scripts/check_golden_baseline.py` — **FAIL**: `experiments/e001.json` differs from HEAD (live run)
- `scripts/check_data_coverage.py` — **FAIL**: `data/panel.parquet` fingerprint mismatch, not git-tracked, manifest unreadable in temp workspace
- `scripts/validate_template.py`
- `scripts/check_experiment_imports.py` (all drivers' calls/imports OK)
- `verify_convention_robustness.py` (all strategy blocks PASS)

Unit tests requiring `numpy`/`pandas`/`pytest` are not runnable in this sandbox (deps absent); this is environmental and unrelated to repo content.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote; note `__pycache__`/handoff noise is expected.
2. **Recovery required**: Ensure `.verify_snapshot/` is absent. A stale snapshot exists in the temp workspace (pid 999999) and a live run (pid 58418) has modified goldens. Run:
   ```
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (or restore pinned goldens per `AGENTS.md`: `git checkout -- experiments/`) before other work.
3. Resolve `data/panel.parquet` coverage issue: the file is not git-tracked and its fingerprint differs from the pinned baseline. If the committed snapshot is authoritative, ensure it is present and tracked; otherwise re-pin with `python3 scripts/check_data_coverage.py --update` **only with explicit direction and ledger justification**.
4. `pip install -r requirements.txt` if deps are missing (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; pytest for tests).
5. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`** (walk-forward + placebo RNG).
- Scopes (`AGENTS.md`):
  - `make check` / `SEED=42 bash scripts/check.sh` (~seconds, offline)
  - `SEED=42 python3 verify_convention_robustness.py` (reads JSONs, no writes)
  - `SEED=42 python3 run_all_verification.py` (quick, ~8 min)
  - `SEED=42 python3 run_all_verification.py --extended` (~21 min)
  - `SEED=42 python3 run_all_verification.py --full` (~15 min)
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- Interrupted-run recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit verification output over canonical `experiments/*.json` goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer must create it via GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (research complete E001–E051; handoff refreshes through E390)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T18-59-50Z_INITIAL_TASK.md` (repo root), mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Supersedes operationally:** `handoff_2026-11-15T18-56-32Z_INITIAL_TASK.md` and earlier handoffs (retained for history).
- Generic handoff pointers repointed to this artifact via `scripts/repoint_handoff.py`.
- No code, experiments, ledgers, or baselines modified for this handoff refresh (aside from this deliverable and its ledger entry).