# Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp:** 2026-11-19T21:14:16Z
**Prepared by:** prior session (handoff refresh, no research performed)
**Repository HEAD at creation:** `cc9b8c25` (`chore(kilo): checkpoint agent session`), equal to `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial Task Message

> You are starting a fresh agentic work session in this repository. First orient
> yourself and confirm the canonical baselines are intact. Do **not** start new
> research, re-pin goldens/data, or commit anything until the user gives an
> explicit task. When you finish, leave your own timestamped handoff using the
> procedure below.

## Start-Here Checklist (in order)

1. **Orient.** Read `AGENTS.md` (project commands, conventions, integrity rules)
   and `ledger/RESEARCH_LEDGER.md` (experiment dispositions; read the tail for
   the most recent entries). Confirm `git rev-parse HEAD origin/main` agree.
2. **Recover any interrupted verification.** If `.verify_snapshot/` exists,
   run `SEED=42 python3 run_all_verification.py --restore-only` before anything
   else. Never leave a verification run half-finished.
3. **Confirm both golden guards pass:**
   - `python3 scripts/check_goldens_clean.py` → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
4. **Provision dependencies** if needed: `pip install -r requirements.txt`
   (numpy/pandas/scipy are not importable on a fresh runner).
5. **Run the fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`).
   It is offline and takes seconds-to-minutes.
6. **Wait for an explicit user task.** Do not invent research scope from this
   handoff; the research phase is closed.
7. **Leave your own handoff** at the end (see *Handoff Procedure*).

## Current Verified State (at creation of this file)

- HEAD `cc9b8c257c1c9f4b1b32905c1497e8dcc24189b6` on `main`, equal to `origin/main`.
- Working tree clean apart from gitignored `__pycache__/*.pyc` churn and the new
  (uncommitted) handoff artifacts.
- No `.verify_snapshot/`, no `.verify_reports/` — no interrupted verification run.
- `scripts/check_goldens_clean.py`: **passed** (exit 0).
- `scripts/check_golden_baseline.py`: **passed** (107/107 pinned artifacts).
- `git diff HEAD -- experiments/`: empty at last confirmed check.
- Research phase remains closed (E001–E043 published; ledger handoff refreshes
  run through E556 and this file is E557).

## Verification Scopes

```bash
SEED=42 bash scripts/check.sh                 # convention + template + guards (fast, offline)
SEED=42 python3 run_all_verification.py       # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended   # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover golden artifacts
```

## Integrity Rules (do not violate)

- `experiments/*.json` are canonical. Verification backs them up and restores
  them; never commit verification output or a half-finished run.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a
  side effect of running the suite. Re-pinning is a deliberate, reviewed act.
- Known, accepted drift: E041 (1-ulp ill-conditioned QP, ~133 numeric diffs) and
  E042 grid artifacts. Do **not** re-pin them to silence the report (ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention; report
  overnight decomposition alongside.
- Keep commits out unless the user explicitly asks for one.

## Key References

- `AGENTS.md` — commands, conventions, baseline-integrity policy.
- `ledger/RESEARCH_LEDGER.md` — experiment results and open items.
- `ledger/PRIORITIZATION.md` — ranking criteria (research phase is closed).
- `scripts/check.sh`, `run_all_verification.py`, `verify_convention_robustness.py`.
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py`.

## Open Items / Known Constraints

- E041/E042 tangency QP remains ill-conditioned; drift is documented and
  intentionally not masked (ledger E049).
- `cvxpy`/`cvxopt` are optional; the optimizer falls back to `scipy.optimize`.
- The CI workflow file cannot be created by automated agents; use the template
  in `.github/workflow-templates/verification-gate.yml` (see
  `VERIFICATION_GATE_TEMPLATE.md`).

## Handoff Procedure (for the next session)

1. Write `handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md` at the repo root
   (use `YYYY-MM-DDTHH-MM-SSZ`, colons replaced by hyphens).
2. Mirror it **byte-identically** into `handoff/`, `HANDOFFS/`, `.handoff/`,
   `.kilo/`, and `.kilo/handoff/`.
3. Repoint the stable aliases: `python3 scripts/repoint_handoff.py <new-file>`,
   then `python3 scripts/repair_broken_handoff.py <new-file>` if needed.
   Confirm `HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`,
   `handoff.md`, `handoff/CURRENT`, and `.kilo/handoff/CURRENT` resolve to it.
4. Append a ledger entry (next `E###`) under `ledger/RESEARCH_LEDGER.md` recording
   the canonical file, SHA-256, repoint audit, verified state, and constraints
   honored. Leave changes uncommitted unless asked.
