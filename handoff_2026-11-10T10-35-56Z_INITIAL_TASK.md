# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T10:35:56Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `667508ea` (`chore(kilo): durable handoff for next agentic session (2026-11-10T09:24:49Z)`) — in sync with `origin/main`.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` with only ` M src/__pycache__/cache_keys.cpython-312.pyc` (tracked bytecode, pre-existing modification — **do not stage/commit**).
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- No source, experiment, ledger, script, test, or baseline artifact changes observed in this session.
- **Research phase complete (E001–E043).** Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Data note: `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be missing from a fresh working tree (gitignored); `QUANT_RESEARCH_OFFLINE=1` is enforced during verification, so missing pinned cache entries fail hard.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm source state and `HEAD`/remote alignment (note pre-existing `src/__pycache__/cache_keys.cpython-312.pyc` modification if still present).
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
- Do not stage/commit bytecode (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T10-35-56Z_INITIAL_TASK.md` (root), mirrored via canonical symlinks.
- **Supersedes (operationally):** `handoff_2026-11-10T09-28-54Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).

(End of file)