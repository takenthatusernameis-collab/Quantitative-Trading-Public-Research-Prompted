# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T20:16:50Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — verified clean at handoff creation
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- Repository is in a closed/research-complete state (E001–E043). Dispositions in `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Do not modify or re-pin as a side effect of routine verification.
- `.verify_snapshot/` absent (no interrupted verification). If present, run `SEED=42 python3 run_all_verification.py --restore-only` first.
- Closed/resolved — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. Do not re-pin those artifacts.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and note HEAD vs origin/main.
2. Confirm `.verify_snapshot/` absent; restore if stale.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; never commit verification output; restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)

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

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent.

## Handoff Provenance

- Supersedes prior timestamped handoffs (retained as history).
- Durable artifact: `handoff_2026-11-07T20-16-50Z_INITIAL_TASK.md`.
