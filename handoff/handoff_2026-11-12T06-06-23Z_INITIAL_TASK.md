# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026:11:12T06:06:23ZZ
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `863d4cd1` — tracking `origin/main` (check alignment)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: check current tree state (tracked `__pycache__` modifications may persist; not substantive changes).
- `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` (excluding `__pycache__`): verify no uncommitted research changes.
- `.verify_snapshot/`: absent unless an interrupted verification run is in progress.
- **Research phase complete (E001–E043).** Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity, ~1e-05). **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm `HEAD`/remote alignment and note tracked `__pycache__` modifications. Decide explicitly (with user direction if needed) whether to restore, ignore, or commit them; do not let accidental bytecode changes contaminate substantive commits.
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

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-12T06-06-23Z_INITIAL_TASK.md` (root, mode 0600)
- **Mirrored to:** `handoff/handoff_2026-11-12T06-06-23Z_INITIAL_TASK.md`, `.handoff/handoff_2026-11-12T06-06-23Z_INITIAL_TASK.md`, `.kilo/handoff/handoff_2026-11-12T06-06-23Z_INITIAL_TASK.md`
- **Supersedes:** earlier `handoff_*_INITIAL_TASK.md` and `HANDOFF_NEXT_SESSION_*_INITIAL_TASK.md` handoffs (retained as history).

(End of file - total 55 lines)