# Handoff — Initial Task Message for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T00:36:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main` — in sync with `origin/main`
**HEAD:** `7acb6861` — "chore(kilo): checkpoint agent session"
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Session Summary (this handoff)

This session received only the instruction to leave a durable, timestamped, clear
initial-task handoff message for the next agentic work session. **No substantive
work was performed:** no experiments were run, no code was changed, no
verification was executed, and no commit was made.

### Verified state at handoff time
- `git status --short --branch`: `## main...origin/main`. The only working-tree
  changes are 11 pre-existing tracked `__pycache__/*.pyc` modifications — treat
  as non-source noise; do not commit unless explicitly instructed.
- `.verify_snapshot/`: **absent** — no interrupted verification restore is
  pending. Canonical baselines are authoritative and untouched:
  `experiments/*.json` (committed goldens), `ledger/golden_baseline.json`,
  `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of
  routine verification.
- Research phase is complete (**E001–E043**); dispositions and history live in
  `ledger/RESEARCH_LEDGER.md`.
- `research_state/workflow_run_diagnostics.jsonl` is present (session
  diagnostics only, not a research artifact).

## Clear Initial Task for the Next Session

**Default action: wait for explicit user instructions.** Do not invent
experiments, run verification unprompted, change promotion gates/outcomes, or
modify golden/baseline artifacts without explicit direction.

### If the user requests work, verify state first
1. `git status --short --branch` — confirm `HEAD`/origin state and note any
   local changes (treat stray `__pycache__` diffs as non-source noise).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted:
   `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned
   goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any
   substantive change.

### If asked to run verification
- Use standard commands with `SEED=42`; **never commit verification output** over
  `experiments/*.json`.
- `run_all_verification.py` backs up/restores goldens; if interrupted, restore
  before committing.
- If `scripts/check.sh` reports a golden/baseline mismatch, fix/restore before
  committing.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens
  (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json`
  without explicit, intentional re-baseline instruction and proper process.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism +
  exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift.
  **Do not re-pin** E041/E042 artifacts to silence drift.
- Do not create `.github/workflows/` CI gates as an automated agent (use
  `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification
  expectations, or outcomes without explicit justification and a ledger update.
- `data/panel.parquet` is pinned in `ledger/data_baseline.json` but may be
  missing from a fresh working tree (gitignored); do not re-pin without
  explicit direction.

## Handoff Provenance

- **Durable artifact (this session):**
  `handoff_2026-11-10T00-36-00Z_INITIAL_TASK.md` (root, working-tree durable;
  not committed). Canonical symlinks `handoff_CURRENT*`, `handoff_LATEST*`,
  `handoff_current*`, `handoff_latest*`, `handoff_next*`, `INITIAL_TASK*`,
  `LATEST*`, `NEXT_SESSION*`, `HANDOFF_*` across root, `handoff/`, `HANDOFFS/`,
  `.handoff/`, `.kilo/`, `.kilo/handoff/` repointed to this file.
- **Supersedes (operationally):** `handoff_2026-11-10T00-34-29Z_INITIAL_TASK.md`,
  `handoff_2026-11-10T00-30-57Z_INITIAL_TASK.md`, and all earlier timestamped
  handoffs (retained as history).
- Historical timestamped-named pointers left untouched to preserve history.