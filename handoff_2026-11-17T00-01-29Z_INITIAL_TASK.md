# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-17T00:01:29Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `ff7ac439a5d5` (full: `ff7ac439a5d5086eb8d8797708576ee42faed99b`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean except pre-existing `__pycache__/*.pyc` mtime churn (ignore; do not commit). `git status --short --branch` shows `## main...origin/main` with only modified `__pycache__` files.
- **Sync:** local `main` is in sync with `origin/main` at this HEAD (verify with `git rev-list --left-right --count origin/main...HEAD`).
- **Verification snapshot:** no active/interrupted verification state observed (`.verify_snapshot/`, `.verify_reports/` absent). If either exists, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
- **Baselines/pins:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative; do not re-pin as a side effect of verification.
- **Research phase:** complete (E001–E051). Dispositions, notes, and open/closed items are recorded in `ledger/RESEARCH_LEDGER.md`.
- **Closed items (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05 sensitivity). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Operational supersession:** this handoff supersedes `handoff_2026-11-17T00-00-24Z_INITIAL_TASK.md` operationally; prior handoff files are retained for history.

## Initial task for the next session (CLEAR)

**Default action: wait for explicit user instructions.**
Do not invent experiments, do not run long verification unprompted, do not change promotion gates/outcomes, and do not modify/re-pin golden or baseline artifacts without explicit direction. The repository is in a closed, fully-verified research state.

### Required first steps if you start work

1. `git status --short --branch` and confirm `main...origin/main` alignment (record any divergence).
2. Ensure no stale verification snapshot: if `.verify_snapshot/` is present, run `SEED=42 python3 run_all_verification.py --restore-only` before anything else.
3. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`). If dependencies are missing, `pip install -r requirements.txt`.
4. Review `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for invariants, closed items, and reproduction commands.

### If asked to verify/reproduce

- Always use `SEED=42`.
- Fast guards: `SEED=42 bash scripts/check.sh` / `make check`.
- Read-only convention check: `SEED=42 python3 verify_convention_robustness.py`.
- Full suite options (per `AGENTS.md`): `SEED=42 python3 run_all_verification.py` (`--quick` default behavior), `--extended`, `--full`, or `--skip-slow` as appropriate.
- Verification overwrites then restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before committing.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` unless explicitly directed and justified in the ledger.

### If asked to do repo maintenance

- Prefer minimal, targeted changes. Run `python3 -m py_compile` on changed Python files.
- Do not create `.github/workflows/` via automated agents (template only: `.github/workflow-templates/verification-gate.yml`).
- Never commit secrets/keys.

## Guardrails (must follow)

- Reproducibility: `SEED=42`; respect pinned vintages/caches; verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Baselines/goldens are authoritative; never replace/re-pin as a verification side effect.
- Pre-registration, gates, falsification expectations, and validated constructions remain unchanged; sensitivity grids are reported, not gated; record negative results honestly.
- Closed: do not reopen E049/E050 or treat E041/E042 residual QP drift as actionable re-pinning work.

## Key references

- `AGENTS.md` — commands, invariants, baseline-integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and open/closed items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `experiments/*.json` — canonical golden artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-17T00-01-29Z_INITIAL_TASK.md`
- **Operational pointers:** repoint with `python3 scripts/repoint_handoff.py handoff_2026-11-17T00-01-29Z_INITIAL_TASK.md`
