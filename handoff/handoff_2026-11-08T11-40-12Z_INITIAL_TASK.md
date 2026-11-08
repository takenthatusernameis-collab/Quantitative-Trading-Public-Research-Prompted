# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T11:40:12Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `862817a9c4eb5e0415b1d41fdb2dc59121762795` (`chore(kilo): checkpoint agent session`, 2026-11-08 10:52:31 +0000)
**Remote:** `origin/main` @ identical SHA — in sync
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean (`git status --short --branch` reports no modifications, no untracked files). `.verify_snapshot/` absent (no interrupted verification run to recover).

---

## Current State

- This session performed no technical research work. Action taken: created this durable, timestamped handoff only, in response to the user request to leave a clear initial task message for the next agentic work session.
- Research phase complete (**E001–E110** recorded; see `ledger/RESEARCH_LEDGER.md`). Last ledger entry: **E110** (Durable Handoff Refresh, HEAD `c9c61a45`, 2026-11-08T04:17Z). No open research items.
- Canonical baselines remain authoritative: tracked `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. Do not modify or re-pin as a side effect of routine verification.
- Closed — do not reopen: E049/E050; E041/E042 residual ill-conditioned QP drift. Do not re-pin E041/E042 artifacts to silence drift.
- Delta since prior durable handoff (`handoff_2026-11-08T10-06-35Z_INITIAL_TASK.md`, HEAD `18fd4a52`): HEAD advanced via checkpoint commits to `862817a9`; no research/artifact/code/ledger substance changed.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state; note any untracked handoff files (do not commit unless explicitly instructed).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` before other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; never commit verification output over canonical goldens. Restore goldens after any interrupted run. Follow `AGENTS.md` baseline-integrity rules exactly.

---

## Reproduction / Verification Commands (use only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

---

## Guardrails

- SEED=42 for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and justification.
- Do not reopen closed E049/E050 or E041/E042 drift items; do not re-pin E041/E042 to mask ill-conditioned QP drift.
- Do not create `.github/workflows/` CI gates as an automated agent (template at `.github/workflow-templates/verification-gate.yml` requires a maintainer via GitHub UI).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Keep handoffs durable and factual.

---

## Handoff Provenance

- Created 2026-11-08T11:40:12Z in response to: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*.
- Supersedes operationally: `handoff_2026-11-08T10-06-35Z_INITIAL_TASK.md` (earlier timestamped handoffs retained as history).
- Durable artifact: `handoff/handoff_2026-11-08T11-40-12Z_INITIAL_TASK.md`.

(End of file)