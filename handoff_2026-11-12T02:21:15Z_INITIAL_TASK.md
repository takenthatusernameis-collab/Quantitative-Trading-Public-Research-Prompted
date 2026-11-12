# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T02:21:15Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `c3c8018f69c529dbea6cbaded8f12735017b6270` (`chore(kilo): checkpoint agent session`) — tracking `origin/main` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` with **12 pre-existing tracked modifications only** — `__pycache__/*.pyc` artifacts under `scripts/`, `src/`, and `tests/` (timestamp/byte drift; **do not commit** unless explicitly instructed). No source, experiment, ledger, script, test, or baseline artifact changes.
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- **Research phase complete (E001–E043).** Authoritative history/dispositions: `ledger/RESEARCH_LEDGER.md`. Canonical baselines: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). **Do not re-pin** E041/E042 artifacts to silence drift.
- No actionable open research items in ledger (E001–E051 research; later E052+ entries are durable-handoff refreshes only).
- **Delta vs prior durable handoff (`handoff_2026-11-12T02:19:15Z_INITIAL_TASK.md`, HEAD `cd0c07d9`)**: HEAD advanced to `c3c8018f` via checkpoint commit(s) with no research-substance changes; prior closed/conformance state adopted.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean source state and HEAD/remote alignment (ignore pre-existing `__pycache__` modifications unless asked).
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
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys or `__pycache__` build artifacts.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-12T02:21:15Z_INITIAL_TASK.md` (root).
- **Supersedes (operationally):** `handoff_2026-11-12T02:19:15Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **HEAD at handoff:** `c3c8018f69c529dbea6cbaded8f12735017b6270`.
