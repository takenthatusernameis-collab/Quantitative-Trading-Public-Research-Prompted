# Handoff — Initial Task Message

**Timestamp:** 2026-11-19T21:10:00Z
**Canonical SHA-256:** (computed after write; recorded in the ledger entry E556)
**HEAD at creation:** `6e96c80d3280ec5c1b6f6052beb86e4d4ab2ef95` on `main` at `origin/main` (`chore(kilo): checkpoint agent session`)
**Supersedes as current artifact only:** `handoff_2026-11-19T21-06-52Z_INITIAL_TASK.md`

## Initial Task Message (start here)

No new research task was assigned. The next agentic work session should begin by
confirming the repository is in its known-good state, then take direction from the
user before any change. Work the checklist in order and stop at step 6 until the
user states an objective.

1. `git rev-parse HEAD` and `git status --short`. Expect `main == origin/main`;
   the only dirty paths should be gitignored `__pycache__` `.pyc` churn plus this
   uncommitted handoff artifact.
2. `ls .verify_snapshot .verify_reports` — both must be absent. If either exists,
   an earlier verification run was interrupted: recover with
   `SEED=42 python3 run_all_verification.py --restore-only` before anything else.
3. `python3 scripts/check_goldens_clean.py` and
   `python3 scripts/check_golden_baseline.py`. Both must exit 0
   (all committed artifacts match HEAD; 107/107 pinned goldens match the baseline).
4. Provision dependencies before any Python driver or data step:
   `pip install -r requirements.txt`. At handoff time `numpy`/`pandas`/`scipy`
   were **not** importable on this runner.
5. `SEED=42 bash scripts/check.sh` — fast convention-robustness + template check.
   If it fails, fix the working tree before any commit; a checkpoint captured
   during a verification run silently replaces the canonical baseline.
6. Await an explicit objective from the user. Do not start new research, re-pin
   baselines, or commit on your own initiative.

When this session ends, repeat the recurring handoff procedure below so the next
session starts from a fresh, timestamped artifact.

## Context

- Repository: Quantitative-Trading-Public-Research-Prompted
- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Research phase is complete; surviving validated strategies are recorded in
  `ledger/RESEARCH_LEDGER.md`. Handoff-refresh entries run through E556.
- `AGENTS.md` is the canonical source for commands, verification scopes, and
  baseline-integrity rules. Read it before running anything.

## Verified State At Handoff

- HEAD `6e96c80d` on `main`, identical to `origin/main`.
- `scripts/check_goldens_clean.py` -> "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD" (exit 0).
- `scripts/check_golden_baseline.py` -> "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT" (exit 0).
- `.verify_snapshot/` and `.verify_reports/` absent; no interrupted run to recover.
- `scripts/check.sh` was not executed in the handoff session (dependencies absent).

## Verification Scopes

- `SEED=42 bash scripts/check.sh` — fast convention robustness + template validation.
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min).
- `SEED=42 python3 run_all_verification.py --extended` — quick + 18 more committed drivers.
- `SEED=42 python3 run_all_verification.py --full` — E042 n_sim=50 + sensitivity grid.
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only (no writes).
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after an interruption.

## Integrity Rules

- Never commit verification output. If interrupted, restore goldens first.
- Never re-pin goldens or the data baseline as a side effect of running the suite;
  re-pinning is a deliberate, reviewable change.
- Never commit `__pycache__` or other generated churn.
- The committed golden is the authoritative record, not the latest re-run.

## Key References

- `AGENTS.md` — commands, conventions, baseline-integrity guidance.
- `ledger/RESEARCH_LEDGER.md` — canonical research and handoff record.
- `ledger/golden_baseline.json` — SHA-256 fingerprint of the 107 pinned goldens.
- `ledger/data_baseline.json` — data cache coverage baseline.
- `ledger/PRIORITIZATION.md` — strategy prioritization context.
- `scripts/repoint_handoff.py` — repoints stable aliases to a new handoff artifact.

## Open Items

- E041/E042 grid artifacts drift by 29–133 numeric differences from an
  ill-conditioned QP (1-ulp sensitivity). Do **not** re-pin to silence it.
- E030's pinned 16-ETF panel is committed; do not revert to live downloads.
- E029 requires its pinned fundamentals snapshot in `data/fundamentals/`.
- The intended CI gate cannot be created by automated agents; the template lives
  at `.github/workflow-templates/verification-gate.yml` and a maintainer must add it.

## Recurring Handoff Procedure

1. Verify HEAD == `origin/main`; working tree clean apart from gitignored `__pycache__`.
2. Confirm no `.verify_snapshot/` or `.verify_reports/`.
3. Run `python3 scripts/check_goldens_clean.py` and `python3 scripts/check_golden_baseline.py`; both must exit 0.
4. Write `handoff_<ISO8601>_INITIAL_TASK.md` at the repo root with this structure.
5. Mirror byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
6. Run `python3 scripts/repoint_handoff.py handoff_<ISO8601>_INITIAL_TASK.md` so every stable alias resolves to the new artifact.
7. Append a numbered `Exxx: Durable Handoff Refresh` entry to `ledger/RESEARCH_LEDGER.md`.
8. Do not commit; leave the artifact uncommitted pending explicit direction.

## Constraints Honored

No golden/data baseline re-pinned, no verification output committed, no new research
performed, `__pycache__` not committed, no commit made (left uncommitted pending
explicit direction).
