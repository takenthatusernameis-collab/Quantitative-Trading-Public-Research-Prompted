# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T03:46:17Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `bc3e234` (`chore(kilo): checkpoint agent session`) == `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- **Working tree:** clean (`git status --short --branch` shows `main...origin/main`, no untracked/modified files). No `.pyc` drift this time.
- **HEAD vs origin:** `bc3e234` == `origin/main` (in sync).
- **Goldens:** unchanged baseline; no re-pinning performed this session. 138 tracked artifacts under `experiments/`, all matching HEAD.
- **Verification snapshot:** `.verify_snapshot/` absent; no live owner.
- **Research phase:** complete (E001–E043). Closed items (do not reopen): E049/E050 (optimizer determinism / exact KKT enumeration), E041/E042 ill-conditioned QP drift (do not re-pin to silence residual numeric drift).
- **Ledger:** `ledger/RESEARCH_LEDGER.md` latest entries are E099–E104 (durable-handoff refreshes, 2026-11-05 → 2026-11-07T01:41Z). No new research entries since.

## Session Summary (this session)

- User requested: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"
- Confirmed repo state: HEAD == origin/main (`bc3e234`), clean working tree, no `.verify_snapshot/`.
- The only change since the prior handoff (`handoff_2026-11-07T03-45-13Z_INITIAL_TASK.md`, which pointed at `4b7527c`) is the checkpoint commit `bc3e234`, which committed that prior handoff file plus the canonical-symlink repoints. No substantive code/data/ledger/experiment work.
- Created this fresh timestamped handoff (`2026-11-07T03:46:17Z`) reflecting `bc3e234`, mirrored it to durable locations, and repointed canonical symlinks.
- No verification runs, no code/data/ledger/experiment changes, no baseline re-pinning.

## Initial Task for Next Session (CLEAR)

**Wait for explicit user instructions.** Do not invent new tasks, re-run verification "just to be sure," modify experiments, or change baselines without explicit direction.

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

- Supersedes: `handoff_2026-11-07T03-45-13Z_INITIAL_TASK.md` (pointed at `4b7527c`).
- Durable copies: repo root, `handoff/`, `.handoff/`, `.kilo/handoff/`.
- Canonical symlinks repointed to this artifact.

(End of file)