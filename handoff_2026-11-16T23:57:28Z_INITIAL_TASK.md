# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T23:57:28Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `dd017737fb42` (`dd017737fb42350513b9dddb10d6f858be3a85b1`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean except pre-existing gitignored `__pycache__/*.pyc` mtime churn (ignore). `git status --short --branch` shows `## main...origin/main` with only those cache-file noise entries if present.
- **Verification snapshot:** no active/interrupted verification state observed (`.verify_snapshot/`, `.verify_reports/` absent). If either exists, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
- **Baselines/pins intact:** `ledger/golden_baseline.json` (107 artifacts) and `ledger/data_baseline.json` (35 pinned data files) are authoritative; do not re-pin as a side effect of verification.
- **Research phase:** complete (E001–E043). Dispositions and notes in `ledger/RESEARCH_LEDGER.md`.
- **Closed items (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 to silence drift.
- **Check context:** `SEED=42 bash scripts/check.sh` was exercised in this environment; static/pinning guards and unit-test runs proceeded, but environment may lack `pandas` (causing `tests/test_data_coverage.py` import errors) and repo fixtures include intentional negative `data/panel.parquet` cases in temp-dir checks — treat only real repo failures as regressions. Install deps with `pip install -r requirements.txt` if needed.
- **Supersedes operationally:** `handoff_2026-11-16T23:55:20Z_INITIAL_TASK.md` (retained for history).

## Initial task for the next session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run long verification unprompted, change promotion gates/outcomes, or modify/re-pin golden or baseline artifacts without explicit direction. The repository is in a closed, fully-verified research state.

### If you start work (required first steps)

1. `git status --short --branch` and confirm `main...origin/main` alignment (or record divergence).
2. Ensure no stale verification snapshot: if `.verify_snapshot/` present, run `SEED=42 python3 run_all_verification.py --restore-only` before anything else.
3. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`). If dependencies are missing, `pip install -r requirements.txt`.

### If asked to verify/reproduce

- Always use `SEED=42`.
- Use `make check` / `scripts/check.sh` for fast guards; `python3 verify_convention_robustness.py` read-only; `python3 run_all_verification.py` with `--quick` (default), `--extended`, or `--full` per `AGENTS.md`.
- Verification overwrites then restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before committing.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` unless explicitly directed and justified in the ledger.

### If asked to do repo maintenance

- Prefer minimal, targeted changes. Run `python3 -m py_compile` on changed Python files.
- Do not create `.github/workflows/` via automated agents (template only at `.github/workflow-templates/verification-gate.yml`).
- Never commit secrets/keys.

## Guardrails (must follow)

- Reproducibility: `SEED=42`, respect pinned vintages/caches; suite uses `QUANT_RESEARCH_OFFLINE=1`.
- Baselines/goldens are authoritative; never replace/re-pin as a verification side effect.
- Pre-registration and goalposts unchanged; sensitivity grids reported, not gated; record negatives honestly.
- Closed: do not reopen E049/E050 or E041/E042 drift.

## Key references

- `AGENTS.md` (commands, invariants)
- `ledger/RESEARCH_LEDGER.md` (dispositions/open items)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `experiments/*.json`
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this file):** `handoff_2026-11-16T23:57:28Z_INITIAL_TASK.md`
- **Operational pointers:** repoint with `python3 scripts/repoint_handoff.py handoff_2026-11-16T23:57:28Z_INITIAL_TASK.md`.
