# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T06:56:17Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `df3efeecbfd3965c0e190d2a51a5f655020d8bd2` (`chore(kilo): checkpoint agent session`, 2026-11-08 06:55:43 +0000)
**Remote:** `origin/main` (verify with `git status --short --branch` before work)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** working tree clean; `.verify_snapshot/` **absent** (no interrupted verification run to recover).

---

## Current State

- **This session performed no technical research work.** Action taken: created this durable, timestamped handoff only, in response to the user request to leave a clear initial task message for the next agentic work session.
- Research phase is complete (**E001–E110** recorded; see `ledger/RESEARCH_LEDGER.md`). No open research items.
- Canonical baselines remain authoritative: `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- **Delta since prior durable handoff** (`HANDOFF_NEXT_SESSION_2026-11-08T06-51-15Z.md`, HEAD `617cdcf6`): HEAD advanced via checkpoint commits (latest `df3efeec`, 2026-11-08 06:55:43Z). No source, test, experiment, data, script, or ledger research substance changed; handoff/checkpoint maintenance only.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state. **Do not commit** pre-existing modified tracked `__pycache__/*.pyc` artifacts unless explicitly instructed.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over canonical goldens. Restore goldens after any interrupted run. Follow `AGENTS.md` baseline-integrity rules exactly.

---

## Reproduction / Verification Commands (use only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py              # quick (~8 min)
```
