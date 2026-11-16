# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T23:54:31Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `f6e7d0131ef1859b0e0294a64e03901dd937bf19` (verify with `git rev-parse --short=12 HEAD` if unsure)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean except pre-existing gitignored `__pycache__/*.pyc` mtime churn (ignore). `git status --short --branch` should show `## main...origin/main` with only those untracked/modified cache files if anything.
- **Verification snapshot:** no active/interrupted verification state expected (`.verify_snapshot/`, `.verify_reports/` absent). If either exists, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
- **Baselines/pins intact:** `ledger/golden_baseline.json` (107 artifacts) and `ledger/data_baseline.json` (35 pinned data files) are the authoritative pins; do not re-pin as a side effect of verification.
- **Research phase:** complete (E001–E043). Dispositions and notes live in `ledger/RESEARCH_LEDGER.md`.
- **Closed items (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 to silence drift.
- **Latest prior durable handoff (for context):** `handoff_2026-11-16T23:01:10Z_INITIAL_TASK.md` (superseded operationally by this file).

## Initial task for the next session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run long verification unprompted, change promotion gates/outcomes, or modify/re-pin golden or baseline artifacts without explicit direction.

### If you start work (required first steps)

1. `git status --short --branch` and confirm `main...origin/main` alignment (or record divergence).
2. Ensure no stale verification snapshot: if `.verify_snapshot/` present, run `SEED=42 python3 run_all_verification.py --restore-only` before anything else.
3. Before committing substantive changes, run: `SEED=42 bash scripts/check.sh` (or `make check`). If deps missing, `pip install -r requirements.txt`.
   - Note (environment-only, not a repo defect): in some sandboxes `tests/test_data_coverage.py` may error if `pandas` is missing; also the “expected negative-test fixture” lines about `data/panel.parquet` in that script are intentional negative tests (created in a temp dir), not real missing repo data.

### If asked to verify/reproduce

- Always use `SEED=42`.
- Use `make check` / `scripts/check.sh` for fast guards; `python3 verify_convention_robustness.py` for read-only robustness; `python3 run_all_verification.py` with `--quick` (default), `--extended`, or `--full` per `AGENTS.md`.
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

- **Durable artifact (this file):** `handoff_2026-11-16T23:54:31Z_INITIAL_TASK.md`
- **Operational pointers:** repoint with `python3 scripts/repoint_handoff.py handoff_2026-11-16T23:54:31Z_INITIAL_TASK.md` (done in this session).

(End of file)
