# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T01-09-46Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff):** working tree clean.

## Current State (verified)

- `.verify_snapshot/`: absent — no interrupted/pending verification run to recover.
- Canonical baselines authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Do not modify or re-pin as side effect.
- Research phase complete (E001–E043); dispositions in `ledger/RESEARCH_LEDGER.md`. Closure through E109; no open research items.
- Closed/resolved — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. Do not re-pin those artifacts.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch`
2. Confirm `.verify_snapshot/` absent; if stale, `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` before committing any substantive change.

**If asked to run verification:** standard commands; never commit verification output; restore goldens after interrupted run.

## Guardrails

- SEED=42 for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens.
- Never re-pin baselines without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as automated agent.

(End of file)
