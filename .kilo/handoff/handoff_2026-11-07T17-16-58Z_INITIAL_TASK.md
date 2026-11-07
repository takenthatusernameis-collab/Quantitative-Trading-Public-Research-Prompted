# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-07T17:16:58Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `8ba11da9264e46667467c3a0a162fd50e3d4a436` (`chore(kilo): checkpoint agent session`, 2026-11-07 17:15:13 +0000); `origin/main` in sync (identical SHA).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation)

- `git status --short --branch`: **clean** on `main`, in sync with `origin/main`. Zero uncommitted/untracked changes outside the handoff symlink tree.
- `git diff --name-only 26909359..8ba11da9`: only `ledger/RESEARCH_LEDGER.md` (this entry, E107) plus the handoff symlink repoint tree — no source, test, experiment, data, or script changes.
- `.verify_snapshot/`: **absent** — no interrupted or pending verification run to recover.
- Canonical baselines authoritative: `experiments/*.json` (138 tracked golden artifacts, all matching HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- Research phase complete (**E001–E043** surviving strategies; E044–E107 conformance/handoff entries). Dispositions in `ledger/RESEARCH_LEDGER.md` (last entry E107).
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

- **Supersedes (recent):** `handoff_2026-11-07T17-10-08Z_INITIAL_TASK.md`, `handoff/HANDOFF_NEXT_SESSION_2026-11-07T16-37-56Z.md`, `handoff_2026-11-07T16-35-08Z.md`, `.handoff/handoff_2026-11-07T17-10-08Z_INITIAL_TASK.md`, and all earlier timestamped handoffs back to `2026-11-02`.
- **Durable copies:** repo root (`handoff_2026-11-07T17-16-58Z_INITIAL_TASK.md`), `handoff/`, `.handoff/`, `.kilo/handoff/` (identical SHA-256 across all four).
- **Canonical pointers repointed:** all generic canonical symlinks across root, `.handoff/`, `handoff/`, `.kilo/`, `.kilo/handoff/` now resolve to this artifact. Re-scan for broken/`-xtype l` symlinks: **0**.

(End of file - total 52 lines)