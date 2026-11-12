# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T15:19:44Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `4449cd85` (`chore(kilo): checkpoint agent session`) — `main...origin/main` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Working tree:** clean except tracked `__pycache__/*.pyc` byte/timestamp drift (modified, not staged): `scripts/__pycache__/{check_data_coverage,check_golden_baseline,check_goldens_clean,check_json_artifacts,diff_golden}.cpython-312.pyc`, `src/__pycache__/{cache_keys,data}.cpython-312.pyc`, `tests/__pycache__/{test_data_coverage,test_drift_report,test_golden_baseline,test_goldens_guard,test_json_guard}.cpython-312.pyc`. Build noise only; no source, experiment, ledger, script source, test source, or config edits. `git diff HEAD -- experiments/ data/ ledger/` is **empty**.
- **`.verify_snapshot/`:** absent — no interrupted verification run to recover.
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items: `ledger/RESEARCH_LEDGER.md`.
- **Canonical baselines (authoritative):** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json` — do not modify or re-pin during routine verification.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration), E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment. Treat tracked `__pycache__/*.pyc` drift explicitly (restore/discard/commit only with explicit direction); do not let bytecode changes contaminate substantive commits.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. In this sandbox `/usr/bin/python3` may lack `requirements.txt` deps (numpy/pandas/scipy/etc.), so some tests can fail with `ModuleNotFoundError`; install deps (`pip install -r requirements.txt`) before trusting dependency-sensitive checks.

### If asked to run verification

- Always use **`SEED=42`**.
- Use `SEED=42 python3 run_all_verification.py` (quick), `--extended`, or `--full` as appropriate.
- **Never commit verification output** over `experiments/*.json`.
- If a run is interrupted, restore goldens before committing (`--restore-only`; `git checkout -- experiments/` only when HEAD holds the pinned baseline).
- If guards report golden/baseline mismatch, fix/restore before committing — **do not re-pin to silence drift**.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-12T15-19-44Z_INITIAL_TASK.md` (root).
- **Operational pointers:** generic handoff aliases repointed to this artifact via `python3 scripts/repoint_handoff.py handoff_2026-11-12T15-19-44Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-12T15-18-36Z_INITIAL_TASK.md` and prior handoff artifacts/symlinks (retained for history).
