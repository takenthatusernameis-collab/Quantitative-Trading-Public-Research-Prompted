# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-17T03:16:15Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `270ba5ad1ff5` (verify with `git rev-parse --short=12 HEAD` if unsure)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean. `git status --short --branch` → `## main...origin/main` with no modified/untracked entries. (Pre-existing tracked `__pycache__/*.pyc` mtime churn is gitignored and not staged — do not commit bytecode noise.)
- **Sync:** `git rev-parse origin/main` == HEAD (`270ba5ad1ff54e6479916c03967fe69b1935de63`) and `git rev-list --left-right --count origin/main...HEAD` → `0	0` (in sync).
- **Commits since last durable handoff (`62c47a5d` → `270ba5ad`):** one commit, `270ba5ad` (`chore(kilo): checkpoint agent session`). Delta is checkpoint/handoff bookkeeping only (touches `.handoff/`, `.kilo/`, `handoff/`, `HANDOFFS/`, root symlinks, `ledger/RESEARCH_LEDGER.md`, and the prior handoff artifacts) — no changes to `experiments/`, `data/`, `src/`, `scripts/`, or `tests/`.
- **Verification snapshot:** none active/interrupted (`.verify_snapshot/` and `.verify_reports/` both absent). If either appears, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
- **Baselines/pins intact:** `ledger/golden_baseline.json` and `ledger/data_baseline.json` are authoritative; never re-pin as a side effect of verification.
- **Research phase:** complete (E001–E051 research; E052+ durable-handoff refreshes). Dispositions and open items are in `ledger/RESEARCH_LEDGER.md` (last logged entry E429; this refresh appends E430).
- **Closed items (do not reopen):** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 to silence drift.
- **Supersedes operationally:** `handoff_2026-11-17T03:13:08Z_INITIAL_TASK.md` (retained for history).

## Initial task for the next session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run long verification unprompted, change promotion gates/outcomes, or modify/re-pin golden or baseline artifacts without explicit direction. The repository is in a closed, fully-verified research state.

### If you start work (required first steps)

1. `git status --short --branch` and confirm `main...origin/main` alignment (or record divergence).
2. Ensure no stale verification snapshot: if `.verify_snapshot/` present, run `SEED=42 python3 run_all_verification.py --restore-only` before anything else.
3. Before committing substantive changes, run `SEED=42 bash scripts/check.sh` (or `make check`). If deps missing, `pip install -r requirements.txt`.
   - Environment-only note: `tests/test_data_coverage.py` may error if `pandas` is missing; `data/panel.parquet` fixture lines are intentional negative tests in a temp dir, not real missing repo data.

### If asked to verify/reproduce

- Always use `SEED=42`.
- Use `make check` / `scripts/check.sh` for fast guards; `python3 verify_convention_robustness.py` read-only; `python3 run_all_verification.py` `--quick` (default), `--extended`, or `--full` per `AGENTS.md`.
- Verification overwrites then restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before committing.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` unless explicitly directed and justified in the ledger.

### If asked to do repo maintenance

- Prefer minimal, targeted changes. Run `python3 -m py_compile` on changed Python files.
- Do not create `.github/workflows/` via automated agents (template only at `.github/workflow-templates/verification-gate.yml`).
- Never commit secrets/keys.

## Guardrails (must follow)

- Reproducibility: `SEED=42`, respect pinned vintages/caches; suite uses `QUANT_RESEARCH_OFFLINE=1`.
- Baselines/goldens authoritative; never replace/re-pin as a verification side effect.
- Pre-registration and goalposts unchanged; sensitivity grids reported, not gated; record negatives honestly.
- Closed: do not reopen E049/E050 or E041/E042 drift.

## Key references

- `AGENTS.md` (commands, invariants)
- `ledger/RESEARCH_LEDGER.md` (dispositions/open items)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `experiments/*.json`
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this file):** `handoff_2026-11-17T03:16:15Z_INITIAL_TASK.md`
- **Operational pointers:** repoint with `python3 scripts/repoint_handoff.py handoff_2026-11-17T03:16:15Z_INITIAL_TASK.md`.

(End of file - total 62 lines)