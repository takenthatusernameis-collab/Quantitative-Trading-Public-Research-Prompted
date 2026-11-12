# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T14-06-04Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `d82c28ade15567963ed58c590d3b572d83abe7ad` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` (tracking; no divergence observed at handoff time)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff time)

- **Working tree:** no source, experiment, ledger, data, or config edits. Tracked bytecode/timestamp drift only in `__pycache__` files: `scripts/__pycache__/check_data_coverage.cpython-312.pyc`, `scripts/__pycache__/check_golden_baseline.cpython-312.pyc`, `scripts/__pycache__/check_goldens_clean.cpython-312.pyc`, `scripts/__pycache__/check_json_artifacts.cpython-312.pyc`, `scripts/__pycache__/diff_golden.cpython-312.pyc`, `src/__pycache__/cache_keys.cpython-312.pyc`, `src/__pycache__/data.cpython-312.pyc`, `tests/__pycache__/test_data_coverage.cpython-312.pyc`, `tests/__pycache__/test_drift_report.cpython-312.pyc`, `tests/__pycache__/test_golden_baseline.cpython-312.pyc`, `tests/__pycache__/test_goldens_guard.cpython-312.pyc`, `tests/__pycache__/test_json_guard.cpython-312.pyc`. Treat as build noise: do not commit, and do not let contaminate a substantive commit. Handle explicitly (restore/discard/commit) only with explicit direction.
- **`.verify_snapshot/`:** absent — no interrupted verification run pending, no recovery needed.
- **Canonical baselines intact:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json` unchanged.
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items: `ledger/RESEARCH_LEDGER.md`; prioritization: `ledger/PRIORITIZATION.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)
1. `git status --short --branch` — confirm HEAD/remote alignment; handle tracked `__pycache__` modifications explicitly (do not let bytecode changes contaminate substantive commits).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If asked to run verification
- Always use **`SEED=42`**.
- Use `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate.
- **Never commit verification output** over `experiments/*.json`.
- If a run is interrupted, restore goldens before committing (`--restore-only`; `git checkout -- experiments/` only when HEAD holds the pinned baseline).
- If guards report golden/baseline mismatch, fix/restore before committing — **do not re-pin to silence drift**.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_NEXT_SESSION_2026-11-12T14-06-04Z_INITIAL_TASK.md` (repo root).
- **Operational pointers updated:** common root "latest/current/initial_task/next" convenience symlinks repointed to this artifact.
- **Supersedes operationally:** `HANDOFF_NEXT_SESSION_2026-11-12T14-04-34Z_INITIAL_TASK.md`, `handoff_2026-11-12T14-03-02Z_INITIAL_TASK.md`, `HANDOFF-2026-11-12T13:11:49Z.md`, and earlier timestamped handoffs (retained for history).
- This session created the durable handoff artifact only. No code, experiments, ledgers, baselines, data, or source files were modified.

(End of handoff)