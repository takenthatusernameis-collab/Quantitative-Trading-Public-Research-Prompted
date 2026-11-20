# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-20T02:43:10Z
**Prepared by:** prior session (handoff refresh only; no research performed)
**Repository HEAD at creation:** `1d1595e8` (`chore(kilo): checkpoint agent session`), equal to `origin/main`
**Branch:** `main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial Task Message (read this first)

> You are starting a fresh agentic work session in this repository. Orient
> yourself and confirm the canonical baselines are intact. Do **not** start new
> research, re-pin goldens/data, run the verification suite, or commit anything
> until the user gives an explicit task. The research phase is closed (E001–E043).
> When you finish, leave your own timestamped handoff using the procedure at the bottom.

## Start-Here Checklist (in order)

1. **Orient.** Run `git log --oneline -3` and `git status --porcelain`. Read `AGENTS.md`
   (commands, conventions, baseline-integrity rules) and the tail of
   `ledger/RESEARCH_LEDGER.md` (latest experiment and handoff-refresh entries).
   Confirm `git rev-parse HEAD origin/main` agree.
2. **Recover any interrupted verification.** If `.verify_snapshot/` exists or
   `experiments/*.json` differ from HEAD, run
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
   **before** anything else. A verification run must never be left half-finished.
3. **Confirm both golden guards pass** (fast, offline):
   - `python3 scripts/check_goldens_clean.py` -> "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py` -> "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
4. **Provision dependencies if needed:** `pip install -r requirements.txt`
   (`numpy`/`pandas`/`scipy` are not importable on a fresh runner).
5. **Run the fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`).
6. **Do the user's task, or stop.** Do not invent scope from this handoff.
7. **Leave your own handoff** at the end (see *Handoff Procedure*).

## Current Verified State (at creation of this file)

- HEAD `1d1595e8c184f5d0bf868de2fef4c91c1086a9ac` on `main`, equal to `origin/main`.
- Working tree dirty only in tracked `__pycache__/*.pyc` files (ignored build noise)
  plus this new (uncommitted) handoff artifact and its ledger entry.
- No `.verify_snapshot/`, no `.verify_reports/` — no interrupted verification run.
- `git diff HEAD -- experiments/`: empty.
- Both golden guards pass: 107/107 pinned artifacts match `ledger/golden_baseline.json`;
  committed goldens match HEAD.
- Research phase remains closed (E001–E043 published).

## Verification Scopes

```bash
SEED=42 bash scripts/check.sh                          # convention + template + guards (fast, offline)
SEED=42 python3 run_all_verification.py                # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only # recover golden artifacts
```

## Integrity Rules (do not violate)

- `experiments/*.json` are canonical. Verification backs them up and restores
  them; never commit verification output or a half-finished run.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as
  a side effect of running the suite. Re-pinning is a deliberate, reviewed act
  with explicit direction and ledger justification.
- Known, accepted drift: E041 (1-ulp ill-conditioned QP, ~133 numeric diffs) and
  E042 grid artifacts. Do **not** re-pin them to silence the report (ledger E049).
- Closed items — do not reopen: E049/E050 (optimizer determinism + exact KKT
  enumeration) and E041/E042 residual ill-conditioned QP drift.
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention; report
  overnight decomposition alongside.
- Never commit secrets/keys; never log secrets.
- Keep commits out unless the user explicitly asks for one.

## Key References

- `AGENTS.md` — commands, conventions, baseline-integrity policy.
- `ledger/RESEARCH_LEDGER.md` — experiment results and open items.
- `ledger/PRIORITIZATION.md` — ranking criteria (research phase is closed).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `scripts/check.sh`, `run_all_verification.py`, `verify_convention_robustness.py`.
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py`.

## Open Items / Known Constraints

- E041/E042 tangency QP remains ill-conditioned; drift is documented and
  intentionally not masked (ledger E049).
- `cvxpy`/`cvxopt` are optional; the portfolio optimizer falls back to
  `scipy.optimize`.
- The CI workflow file cannot be created by automated agents; use the template
  in `.github/workflow-templates/verification-gate.yml` (see
  `VERIFICATION_GATE_TEMPLATE.md`; maintainer action required).
- The repo root accumulates many historical `HANDOFF*` / `handoff*` artifacts;
  only the stable aliases (`HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`,
  `NEXT_SESSION.md`, `handoff.md`, `handoff/CURRENT`, `.kilo/handoff/CURRENT`)
  track the current one. Do not treat timestamped files as authoritative.
- The ledger's last recorded entry before this refresh is E567
  (`handoff_2026-11-20T02-41-33Z_INITIAL_TASK.md`, HEAD `73226b18`); HEAD has
  since advanced through checkpoint commits only (`1d1595e8`). This refresh adds E568.

## Handoff Procedure (for the session that follows this one)

1. Write `handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md` at the repo root
   (`YYYY-MM-DDTHH-MM-SSZ`, colons replaced by hyphens).
2. Mirror it **byte-identically** into `handoff/`, `HANDOFFS/`, `.handoff/`,
   `.kilo/`, and `.kilo/handoff/`.
3. Repoint the stable aliases:
   `python3 scripts/repoint_handoff.py handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md`,
   then `python3 scripts/repair_broken_handoff.py <new-file>` if needed.
   Confirm `HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`,
   `handoff.md`, `handoff/CURRENT`, and `.kilo/handoff/CURRENT` resolve to it.
   Note: never run `scripts/repoint_handoff.py` without an explicit new-file
   argument — the default target is a historical artifact.
4. Append a ledger entry (next `E###`) under `ledger/RESEARCH_LEDGER.md` with
   the canonical file, SHA-256, repoint audit, verified state, and constraints
   honored. Leave changes uncommitted unless asked.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-20T02-43-10Z_INITIAL_TASK.md`
  (repo root, plus the five byte-identical mirrors above).
- **Supersedes operationally:** `handoff_2026-11-20T02-41-33Z_INITIAL_TASK.md` and
  all earlier `HANDOFF*` / `handoff*` artifacts (retained for history; not altered).
- This session created this durable handoff only. No code, experiments, ledgers
  (other than the new handoff-refresh entry), baselines, or canonical artifacts
  were modified.
