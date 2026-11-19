# Agentic Work Session Handoff — START HERE

**Written:** 2026-11-19T03:43:52Z
**HEAD when written:** `ccf52a08dec90139704deddee3c40338ef8b45cc` (`## main...origin/main`, 0 ahead / 0 behind, tree clean)
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Supersedes:** `handoff_2026-11-19T03-42-52Z_INITIAL_TASK.md` (thin stub) and `handoff_2026-11-19T03-41-35Z_INITIAL_TASK.md` as the current durable artifact. No earlier handoff content is altered.

## Initial Task for the Next Session

There is **no pending code change and no new research task**. The research phase is
closed (E001–E043; ledger entries run through E517). The next session's first
message should be this ordered checklist, executed before anything else:

1. **Orient.** `git rev-parse HEAD`, `git status --short --branch`, and read
   `ledger/RESEARCH_LEDGER.md` tail (last 3 entries) to confirm state.
2. **Recover any interrupted verification.** If `.verify_snapshot/` exists,
   run `SEED=42 python3 run_all_verification.py --restore-only` before doing
   anything else. Confirm `git diff --name-only HEAD -- experiments/` is empty.
3. **Install dependencies** (this runner has bare Python 3.12.3 with **no**
   numpy/pandas/scipy): `pip install -r requirements.txt`.
4. **Run the fast integrity gate:** `SEED=42 bash scripts/check.sh`
   (`make check`). It is offline and takes seconds: convention robustness,
   template validation, golden-clean check, golden-baseline check, data
   coverage, and the portfolio-optimizer determinism test.
5. **Take no further action** until the user gives an explicit instruction.
   Do not re-pin goldens, do not start new experiments, do not commit.
6. **Before ending the session**, leave your own timestamped handoff
   (see "Recurring Handoff Procedure" below).

## Current-State Facts (verified at write time)

- Research phase complete (E001–E043); surviving strategies documented in
  `ledger/RESEARCH_LEDGER.md`.
- HEAD `ccf52a08` matches `origin/main`; working tree clean.
- `.verify_snapshot/` and `.verify_reports/` absent — no interrupted run to recover.
- `git diff --name-only HEAD -- experiments/` → empty; canonical goldens untouched.
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` present and parse.
- `scripts/check.sh` was **not** executed this session (deps unavailable); step 4
  above makes it the next session's first substantive action.

## Verification Commands

```bash
SEED=42 bash scripts/check.sh                 # fast gate (~seconds, offline); = make check
SEED=42 python3 run_all_verification.py       # quick (~8 min); = make verify-quick
SEED=42 python3 run_all_verification.py --extended   # ~21 min; = make verify-extended
SEED=42 python3 run_all_verification.py --full       # ~15 min; = make verify-full
SEED=42 python3 run_all_verification.py --restore-only  # recover after interruption
```

## Integrity Rules (do not violate)

1. **Seed is always 42** (walk-forward + placebo RNG).
2. **A verification run must never be left half-finished** — it overwrites
   `experiments/*.json` and restores them afterward; recover with `--restore-only`.
3. **Never re-pin a golden to silence drift.** Known, root-caused drift:
   E041 (133 numeric diffs, 1-ulp sensitivity of an ill-conditioned QP) and the
   E042 grid (29–133 diffs). These are open ledger items, not bugs to paper over.
4. **Do not commit verification output.** `scripts/check_goldens_clean.py` and
   `scripts/check_golden_baseline.py` must pass before any commit.
5. **Cache coverage is an enforced invariant** — every `data.download()` input
   must be committed and pinned in `ledger/data_baseline.json`.
6. No `__pycache__`, no secrets, no `.github/workflows/` writes (controller-restored;
   use `.github/workflow-templates/`).

## Key Artifacts

- Golden files: `experiments/*.json` (canonical artifacts)
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Baseline pins: `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- Pinned data: `data/vintages.json`, `data/fundamentals_vintages.json`
- Gate template: `.github/workflow-templates/verification-gate.yml`

## Recurring Handoff Procedure

1. Write `handoff_<UTC timestamp>_INITIAL_TASK.md` at the repo root (this file's shape).
2. Mirror byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`;
   confirm all six copies share one SHA-256.
3. `python3 scripts/repoint_handoff.py handoff_<timestamp>_INITIAL_TASK.md`
   (expect ~490 pointers repointed, 0 bad).
4. Append the next `E5xx` entry to `ledger/RESEARCH_LEDGER.md` recording trigger,
   artifact, verification performed, environment note, and constraints honored.
5. Leave the change uncommitted unless the user explicitly asks for a commit.

---
*Durable handoff written at session end for continuity across agentic sessions.*
