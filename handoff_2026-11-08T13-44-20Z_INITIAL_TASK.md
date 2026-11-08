# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T13-44-20Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `502d5787` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified)
- No technical research work performed this session; only this durable handoff was created per explicit request.
- Research phase: **complete** (E001–E043 recorded in `ledger/RESEARCH_LEDGER.md`). No open research items.
- Canonical baselines are authoritative: tracked `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Closed/resolved — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift (do not re-pin E041/E042 artifacts).
- Working tree clean (`git status --short --branch` empty).

## Initial Task for Next Session (CLEAR)
**Default:** wait for explicit user instructions. Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts.

**If work is requested, verify state first:**
1. `git status --short --branch` — confirm clean/expected state.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Before committing substantive changes: `SEED=42 bash scripts/check.sh` (or `make check`).

**If verification is explicitly requested:** use `SEED=42`; never commit verification output over canonical goldens; restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails
- `SEED=42` for reproducibility/verification.
- Never commit driver output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` without explicit re-baseline instruction.
- Do not reopen E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent.

## Provenance
- Created 2026-11-08T13-44-20Z in response to: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Supersedes operationally prior timestamped handoffs (retained as history).
