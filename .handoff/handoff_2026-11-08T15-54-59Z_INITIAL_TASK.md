# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T15:54:59Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `b8f92fd6aa13c3f5b2d10e4092ae4d707fa2e4a3` (`chore(kilo): checkpoint agent session`, 2026-11-08 15:54:26 +0000)
**Remote:** `origin/main` — in sync (verify with `git status --short --branch`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean; zero uncommitted/untracked changes. `.verify_snapshot/` absent (no interrupted verification run to recover). 138 tracked golden artifacts under `experiments/`, all matching HEAD.

---

## Current State

- This session performed no technical research work. Responded to the request to leave a timestamped clear initial task message for the next agentic work session by refreshing this durable handoff against live HEAD.
- Research phase complete (**E001–E110** recorded; see `ledger/RESEARCH_LEDGER.md`). Last ledger entry context: **E110** (Durable Handoff Refresh, HEAD `c9c61a45`, 2026-11-08T04:17Z). No open research items. No OPEN/PENDING/BLOCKED/TODO markers anywhere in the ledger.
- Canonical baselines remain authoritative; do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift (do not re-pin E041/E042).
- Delta since prior handoff (`handoff_2026-11-08T15-52-41Z_INITIAL_TASK.md`, HEAD `379ebd87`): HEAD advanced `379ebd87` → `b8f92fd6` via one commit, `chore(kilo): checkpoint agent session`, touching only the handoff symlink tree (new `handoff_2026-11-08T15-52-41Z_INITIAL_TASK.md` artifact + repointed canonical pointers). **No change to research artifacts, data, src, tests, scripts, or ledger substance.**

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm branch/state.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. If `SEED=42 bash scripts/check.sh` reports golden mismatches, fix/restore before committing — never checkpoint verification output over canonical goldens.

**If asked to run verification:** use standard commands with `SEED=42`; never commit verification output over canonical goldens. Restore goldens after any interrupted run.

---

## Reproduction / Verification Commands (use only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items; do not re-pin E041/E042 to silence ill-conditioned QP drift.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md`; a maintainer must create the workflow via the GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-08T15-52-41Z_INITIAL_TASK.md` and all earlier timestamped handoffs (retained as history).
- **Durable artifact:** root `handoff_2026-11-08T15-54-59Z_INITIAL_TASK.md` + `handoff/handoff_2026-11-08T15-54-59Z_INITIAL_TASK.md`.

(End of file)