# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-21T02-14-16Z
**Prepared by:** session at HEAD `7584f521` (handoff refresh only; no research performed)
**Repository HEAD at creation:** `7584f521050f524a94a9f12e8f729fd59e0a746f` (`chore(kilo): checkpoint agent session`)
**Branch:** `main` (HEAD == `origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial Task Message (read this first)

> You are starting a fresh agentic work session in this repository. Orient
> yourself and confirm the canonical baselines are intact. Do **not** start new
> research, re-pin goldens/data, run the verification suite, or commit anything
> until the user gives an explicit task. The research phase is closed (E001–E043).
> When you finish, leave your own timestamped handoff using the procedure at the bottom.

## Start-Here Checklist (in order)

1. **Orient.** Run `git log --oneline -3` and `git status --porcelain`. Read `AGENTS.md`
   and the tail of `ledger/RESEARCH_LEDGER.md`. Confirm `git rev-parse HEAD origin/main` agree.
2. **Recover any interrupted verification.** If `.verify_snapshot/` exists or
   `experiments/*.json` differ from HEAD, run
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
   before anything else.
3. **Confirm both golden guards pass** (fast, offline):
   - `python3 scripts/check_goldens_clean.py` -> "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py` -> "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
4. **Provision dependencies if needed:** `pip install -r requirements.txt`
5. **Run the fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`).
6. **Do the user's task, or stop.** Do not invent scope from this handoff.
7. **Leave your own handoff** at the end (see *Handoff Procedure*).

## Verification Scopes (only if the user asks to verify)

```bash
SEED=42 bash scripts/check.sh                     # fast convention/guard gate (~seconds)
SEED=42 python3 run_all_verification.py           # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --full    # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 verify_convention_robustness.py   # reads JSONs, no writes
SEED=42 python3 run_all_verification.py --restore-only  # recover after an interrupted run
```

## Integrity Rules (do not violate)

- `experiments/*.json` are canonical. Verification backs them up and restores
  them; never commit verification output or a half-finished run.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as
  a side effect of running the suite.
- Closed items — do not reopen: E049/E050 (optimizer determinism + exact KKT
  enumeration) and E041/E042 residual ill-conditioned QP drift (~1e-5, expected).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- Never commit secrets/keys; never log secrets.
- Keep commits out unless the user explicitly asks for one.

## Key References

- `AGENTS.md` — commands, reproducibility, baseline-integrity policy.
- `ledger/RESEARCH_LEDGER.md` — authoritative experiment record (through E611).
- `ledger/PRIORITIZATION.md` — ranking procedure (active v1.2.3).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 baselines.
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py` — enforcement gates.
- `scripts/repoint_handoff.py`, `scripts/repair_broken_handoff.py` — handoff alias upkeep.

## State Verified This Session

- HEAD `7584f521` (`7584f521050f524a94a9f12e8f729fd59e0a746f`) on `main`, identical to `origin/main`.
- `git diff HEAD -- experiments/` empty (no driver output contaminating the goldens).
- No `.verify_snapshot/`, no `.verify_reports/` (no active/interrupted run).
- Both golden guards executed this session, exit 0:
  - `check_goldens_clean.py` -> "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
  - `check_golden_baseline.py` -> "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
- Working tree clean before this handoff was written (`git status --porcelain` empty).
- This session created this durable handoff only. No code, experiments, baselines,
  or canonical artifacts were modified.

## Carried-Forward Open Items

- E041/E042 residual numeric drift is 1-ulp sensitivity of an ill-conditioned QP.
  Do **not** re-pin to silence it; see the ledger's open item.
- Intended CI gate cannot be created by agents (see AGENTS.md *CI / Automation*);
  a maintainer must add `.github/workflow-templates/verification-gate.yml` via the UI.
- E042-lead artifact drift (SLSQP optimizer sensitivity on the `max_sharpe` branch) is
  the highest-value open item; fixing it means deciding whether the artifact or the
  solver is authoritative — a research decision, not a mechanical repair.

## Handoff Procedure (for the session that follows this one)

1. Write `handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md` at the repo root
   (`YYYY-MM-DDTHH-MM-SSZ`, colons replaced by hyphens).
2. Mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`,
   `.kilo/`, and `.kilo/handoff/`.
3. Repoint the stable aliases:
   `python3 scripts/repoint_handoff.py handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md`,
   then `python3 scripts/repair_broken_handoff.py <new-file>` if needed.
4. Append a ledger entry (next `E###`) under `ledger/RESEARCH_LEDGER.md`.
   Leave changes uncommitted unless asked.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-21T02-14-16Z_INITIAL_TASK.md`
  (repo root, plus the five byte-identical mirrors above).
- Supersedes `handoff_2026-11-21T02-12-45Z_INITIAL_TASK.md` only as the current
  durable artifact. No earlier handoff content or baseline is altered.
- This session created this durable handoff only. No code, experiments, baselines,
  or canonical artifacts were modified.

(End of file)
