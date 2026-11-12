# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T16:06:06Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `839a9782` (`chore(kilo): checkpoint agent session`) — aligned with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (at handoff)
- **Working tree:** `## main...origin/main` with 12 tracked modifications only — all `__pycache__/*.pyc` build artifacts under `scripts/`, `src/`, and `tests/` (byte-identical sizes, timestamp drift; not committed, not substantive). No source, experiment, ledger, script, test, or baseline artifact changes.
- **`.verify_snapshot/`:** absent (no interrupted verification run pending).
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items: `ledger/RESEARCH_LEDGER.md`. Last research entry E051; E052–E172 are durable-handoff refreshes only.
- **Canonical baselines (authoritative):** `experiments/*.json` (138 tracked entries: 107 golden JSONs + 31 drivers), `ledger/golden_baseline.json`, `ledger/data_baseline.json` — do not modify or re-pin during routine verification.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)
**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)
1. `git status --short --branch` — confirm HEAD/remote alignment. Treat tracked `__pycache__` modifications explicitly (restore/discard/commit only with explicit direction); do not let bytecode changes contaminate substantive commits.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

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
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails
- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys; never log secrets.

## Handoff provenance
- **Durable artifact (this session):** `handoff_2026-11-12T16-06-06Z_INITIAL_TASK.md` (root).
- **Operational pointers:** root `handoff_*`/`next_*` convenience symlinks updated to target this artifact where applicable.
- **Supersedes operationally:** `handoff_2026-11-12T16-04-38Z_INITIAL_TASK.md` and prior handoff artifacts/symlinks (retained for history).

(End of handoff)