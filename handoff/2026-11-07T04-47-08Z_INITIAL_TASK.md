# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T04:47:08Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `8037c5f` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean at handoff creation (no uncommitted tracked changes; no `.verify_snapshot/`).
- **HEAD vs origin:** `8037c5f` == `origin/main` (in sync).
- **Goldens:** unchanged canonical baseline; no re-pinning performed this session. Tracked `experiments/*.json` artifacts remain authoritative (see `ledger/golden_baseline.json`).
- **Verification snapshot:** `.verify_snapshot/` absent; no live owner.
- **Research phase:** complete (E001–E043). Closed items (do not reopen): E049/E050 (optimizer determinism / exact KKT enumeration), E041/E042 ill-conditioned QP drift (do not re-pin to silence residual numeric drift).
- **Ledger:** `ledger/RESEARCH_LEDGER.md` latest entries E099–E104 (durable-handoff refreshes). No new research entries.

## Session Summary (this session)

- User requested: “Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !”
- Confirmed repo state: HEAD `8037c5f` == `origin/main`, clean tree, durable handoff directories present (`handoff/`, `.handoff/`, `.kilo/handoff/`), no verification snapshot.
- Reviewed prior durable handoffs (latest `handoff_2026-11-07T04:44:45Z_INITIAL_TASK.md` referenced `72ffe2f`; repo has advanced via checkpoint commits to `8037c5f` with symlink/handoff bookkeeping).
- No verification runs executed. No experiment/code/ledger/golden/data-baseline changes made.
- Created this fresh timestamped durable handoff reflecting current HEAD, mirrored it to durable locations, and repointed canonical latest/initial-task/next-session/handoff symlinks.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent new tasks, re-run verification “just to be sure,” modify experiments, or change baselines without explicit direction.

**If/when asked to do work, verify state first:**
1. `git status --short --branch` and confirm `HEAD == origin/main` (or report divergence).
2. Confirm `.verify_snapshot/` is absent/no live owner. If stale: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing.

**Durable handoff duty:** When the next session completes a user-requested action that should be handed off, create a new timestamped handoff (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`) in repo root, mirror to `handoff/`, `.handoff/`, and `.kilo/handoff/`, and repoint canonical `*_LATEST*`/`INITIAL_TASK*`/`HANDOFF*`/`handoff_next*`/`next_session*` symlinks. Do not create extra handoffs unprompted.

## Do Not

- Do not commit verification output; if interrupted, restore goldens before committing.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a verification side effect.
- Do not re-open closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (controller/token constraints); use local `make check|verify|verify-full`.
- Do not change pre-registered gates/sensitivity grids/outcomes without explicit justification and ledger update.

## Reproduction Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                                   # fast guards (~seconds)
SEED=42 python3 run_all_verification.py                         # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended              # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full                  # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only          # recover goldens after interruption
SEED=42 python3 verify_convention_robustness.py                 # reads JSONs, no writes
```

## Handoff Provenance

- Supersedes: `handoff_2026-11-07T04:44:45Z_INITIAL_TASK.md` (HEAD context advanced to `8037c5f`).
- Durable copies: repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- Canonical symlinks repointed to this artifact.

(End of file)
