# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-08T12:43:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `4f08349a09ea429d3b5fc39e4ac14dc8e4df2cf9` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state (at handoff creation):** `HEAD == origin/main` (in sync). Working tree clean; no uncommitted/untracked changes. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` → empty. `git ls-files experiments/` → 138 tracked golden artifacts, all matching HEAD. `.verify_snapshot/` **absent** (no interrupted verification run to recover).

---

## Current State

- **This session performed no technical research work.** Action taken: created this durable, timestamped handoff only.
- Research phase is complete (E001–E110 recorded; see `ledger/RESEARCH_LEDGER.md`). No open research items.
- Canonical baselines remain authoritative: `experiments/*.json` goldens (138 tracked artifacts, all match HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin** E041/E042 artifacts to silence drift.
- Delta since prior durable handoff (`handoff_2026-11-08T04-17-13Z_INITIAL_TASK.md`, HEAD `c9c61a45`): HEAD advanced via checkpoint commit(s) to `4f08349a`; only the handoff symlink tree changed. No source, test, experiment, data, script, or ledger substance changed.
- **Broken symlink repair performed this session:** 1,890 broken symlinks found (all git-tracked historical `HANDOFF_NEXT_SESSION_*.md` and `INITIAL_TASK`-style pointers in root, `handoff/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`) pointing at the deleted target `../handoff/handoff_2026-11-08T08-02-33Z_INITIAL_TASK.md`. All repointed to `handoff_2026-11-08T12-43-00Z_INITIAL_TASK.md` using per-directory relative targets (root → bare filename; `handoff/` → bare filename; `.handoff/` and `.kilo/` → `../handoff/...`; `.kilo/handoff/` → `../../handoff/...`). Post-repair scan: **0 broken links**.

---

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm state; note pre-existing modified tracked `__pycache__` files and **do not commit them** unless explicitly instructed.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over canonical goldens. Restore goldens after any interrupted run. Follow `AGENTS.md` baseline-integrity rules exactly.

---

## Reproduction / Verification Commands (use only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

---

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (manual/template path: `.github/workflow-templates/verification-gate.yml`, `VERIFICATION_GATE_TEMPLATE.md`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Keep handoffs durable and factual.

---

## Handoff Provenance

- Created 2026-11-08T12:43:00Z in response to: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"* (repeat request; same deliverable as prior sessions).
- **Supersedes operationally:** `handoff_2026-11-08T04-17-13Z_INITIAL_TASK.md` (and earlier timestamped handoffs retained as history).
- **Durable artifact:** `handoff_2026-11-08T12-43-00Z_INITIAL_TASK.md` (root); mirrored to conventional handoff directories and canonical pointers updated where present.