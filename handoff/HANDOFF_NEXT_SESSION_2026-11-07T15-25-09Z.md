# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T15:25:09Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `b453e484 chore(kilo): checkpoint agent session` (`main...origin/main`, no local divergence observed at handoff creation)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- Research phase complete (E001–E043). Dispositions in `ledger/RESEARCH_LEDGER.md`.
- Working tree clean; no uncommitted changes; no `.verify_snapshot/` present (no interrupted verification run).
- Closed/resolved — **do not reopen**: E049/E050, E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts.
- Canonical baselines authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Do not modify or re-pin as a side effect of routine verification.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and `HEAD == origin/main` (or explain divergence).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands from `AGENTS.md` (`make check` / `make verify-quick` / `make verify-extended` / `make verify-full` as appropriate). Never commit verification output. Restore goldens after any interrupted run (`SEED=42 python3 run_all_verification.py --restore-only`).

## Guardrails

- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (controller-managed; template at `.github/workflow-templates/verification-gate.yml`).
- Use `SEED=42` for reproducible runs; follow pre-registration/multiple-testing discipline per `AGENTS.md`.

## Handoff Provenance

- **Supersedes:** `handoff/HANDOFF_NEXT_SESSION_2026-11-07T15-24-08Z.md` (HEAD advanced to `b453e484`).
- **Durable location:** `handoff/HANDOFF_NEXT_SESSION_2026-11-07T15-25-09Z.md`.
