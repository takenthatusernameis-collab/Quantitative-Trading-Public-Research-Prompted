# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T17:10:08Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `26909359a634f771f0a4f1450c72b2ddf993a9af` (`chore(kilo): checkpoint agent session`, 2026-11-07 17:10:37 +0000); `origin/main` in sync (identical SHA).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** on `main`, in sync with `origin/main`. Zero uncommitted/untracked changes.
- `.verify_snapshot/`: **absent** — no interrupted or pending verification run to recover.
- Canonical baselines authoritative: `experiments/*.json` (138 tracked golden artifacts, all matching HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json` (35 pinned data inputs). **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043** surviving strategies; E044–E105 conformance/handoff entries). Dispositions in `ledger/RESEARCH_LEDGER.md` (6305 lines, last entry E105).
- Closed/resolved: **do not reopen** E049/E050 (exact KKT enumeration closed the tangency QP open item) or E041/E042 residual ill-conditioned QP drift; **do not re-pin** E041/E042 artifacts to silence drift.
- No OPEN/PENDING/BLOCKED/TODO markers anywhere in the ledger. Repository closed.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and `HEAD == origin/main` (or explain divergence).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands; **never commit verification output**. Restore goldens after any interrupted run.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds, offline)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py --skip-slow  # convention only
```

## Guardrails

- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use the template/manual maintainer path per repo docs; `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md` are the deliverables).
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.

## Handoff Provenance

- **Supersedes (recent):** `handoff/HANDOFF_NEXT_SESSION_2026-11-07T17-09-46Z.md`, `handoff/HANDOFF_NEXT_SESSION_2026-11-07T17-08-46Z.md`, `.handoff/handoff_2026-11-07T17-10-08Z_INITIAL_TASK.md`, and all earlier timestamped handoffs back to `2026-11-02`.
- **Durable copies:** repo root (`handoff_2026-11-07T17-10-08Z_INITIAL_TASK.md`), `handoff/`, `.handoff/`, `.kilo/handoff/` (identical SHA-256 across all four).
- **Canonical pointers repointed:** all generic canonical symlinks (`HANDOFF_LATEST.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `HANDOFF_NEXT_SESSION_LATEST.md`, `NEXT_HANDOFF.md`, `NEXT_SESSION_HANDOFF.md`, `handoff.md`, `handoff_current.md`, `handoff_latest.md`, `handoff_next.md`, `handoff_next_session.md`, `handoff_next_session_LATEST.md`, `handoff_LATEST_INITIAL_TASK.md`, `INITIAL_TASK_HANDOFF.md`, `handoff__INITIAL_TASK.md`, etc.) now resolve to this artifact. Re-scan for broken/`-xtype l` symlinks: **0**.