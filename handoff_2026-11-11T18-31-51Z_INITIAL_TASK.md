# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-11T18:31:51Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `e21716bf` (`chore(kilo): checkpoint agent session`) — tracking `origin/main`, in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` with **pre-existing tracked `__pycache__/*.pyc` modifications only** (`scripts/__pycache__/*`, `src/__pycache__/data.cpython-312.pyc`, `tests/__pycache__/*`) — **do not commit** unless explicitly instructed. No source, experiment, ledger, script, test, or baseline artifact changes.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Tracked golden artifacts: **107** (`experiments/*.json`). Canonical baselines authoritative: `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Research phase complete (E001–E043).** Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity, ~1e-05). **Do not re-pin** E041/E042 artifacts to silence drift.
- Ledger: no actionable `OPEN|PENDING|BLOCKED|TODO` items. Last research entry E051 (2026-11-02); subsequent durable-handoff refreshes only.
- Reproducibility caveat (`HANDOFF_REPRO_CAVEAT.md`): E041/E042 sensitivity grids and the full E042 confirmatory golden are not byte-reproducible in this sandbox (SLSQP walk-forward optimizer BLAS/LAPACK- and summation-order-sensitive). No gate or decision affected (E041 REJECTED 3/5, E042 PARTIAL 4/5, E042b REJECTED 4/5 under both committed and drifted values).

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm only the known pre-existing `__pycache__` modifications (if any) and `HEAD`/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report a golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never introduce logging of secrets.
- Do not commit pre-existing tracked `__pycache__/*.pyc` working-tree modifications unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-11T18-31-51Z_INITIAL_TASK.md` (root).
- **Supersedes (operationally):** `handoff_2026-11-11T17-51-51Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **HEAD:** `e21716bf` (no research/source/artifact changes made in this handoff session; only this handoff file was written).

(End of file)
