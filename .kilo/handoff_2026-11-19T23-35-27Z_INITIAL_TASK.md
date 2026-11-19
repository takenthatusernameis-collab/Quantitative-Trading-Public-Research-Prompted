# Handoff — Initial Task Message for the Next Agentic Session

**Created:** 2026-11-19T23:35:27Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Verified HEAD at creation:** `448c2a71` (`chore(kilo): checkpoint agent session`), equal to `origin/main`

## Initial task message

You are resuming work on an independent, reproducible quantitative-strategy research
repository. The research phase (E001–E043) is **complete and closed**. Do not start new
research, do not move goalposts, and do not promote or demote a strategy unless the user
explicitly asks for it. Your job in this session is to orient yourself, confirm the
repository is in a clean, reproducible state, complete whatever concrete task the user
gives you, and leave your own timestamped handoff behind.

## Start-here checklist (in order)

1. **Orient.** Run `git log --oneline -3` and `git status --porcelain`. Read `AGENTS.md`
   for conventions, then skim `ledger/RESEARCH_LEDGER.md` (the last entries record the
   handoff refreshes and open items).
2. **Recover any interrupted verification first.** If `.verify_snapshot/ACTIVE.json`
   exists or `experiments/*.json` differ from HEAD, run
   `SEED=42 python3 run_all_verification.py --restore-only` (or
   `git checkout -- experiments/`) before anything else.
3. **Confirm both golden guards.**
   - `python3 scripts/check_goldens_clean.py` → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
   If either fails, fix it before committing anything; never re-pin as a side effect.
4. **Provision dependencies.** `numpy`, `pandas`, and `scipy` are not importable on this
   runner by default. Run `pip install -r requirements.txt` before any Python driver.
5. **Run the fast gate.** `SEED=42 bash scripts/check.sh` (~seconds, offline) — it includes
   the golden guards, data-coverage check, and the portfolio-optimizer determinism test.
6. **Do the user's task.** If no concrete task is given, stop after steps 1–5; do not invent
   research.
7. **Leave your own handoff** using the procedure at the bottom of this file.

## Verification scopes (only if the task requires a full re-run)

```bash
SEED=42 python3 run_all_verification.py            # quick, ~8 min, 8 drivers
SEED=42 python3 run_all_verification.py --extended # +18 drivers, ~21 min
SEED=42 python3 run_all_verification.py --full     # E042 n_sim=50 + sensitivity grid
SEED=42 python3 run_all_verification.py --skip-slow
```

A verification run overwrites `experiments/*.json` and restores them afterward. **Never let
a run end half-finished.** Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.

## Integrity rules (non-negotiable)

- `experiments/*.json` are canonical artifacts. The committed golden is the authoritative
  record, not the latest re-run.
- Replacing a golden requires `python3 scripts/check_golden_baseline.py --update` plus a
  ledger entry, and the re-pin must be visible in the diff. Never re-pin to silence drift.
- Data inputs are pinned; an unpinned input is a live network download and is not
  bit-reproducible. `scripts/check_data_coverage.py` enforces this.
- Do not commit verification output, `__pycache__`, `.verify_snapshot/`, or
  `.verify_reports/`.
- The CI workflow gate cannot be created by automated agents (workflow push permission is
  missing and the controller cleans `.github/workflows/`). The template is at
  `.github/workflow-templates/verification-gate.yml`; a maintainer must create it via the
  GitHub UI.
- Do not commit unless the user explicitly asks.

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline-integrity history.
- `ledger/RESEARCH_LEDGER.md` — every experiment, decision, and handoff entry.
- `ledger/PRIORITIZATION.md` — strategy prioritization.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `VERIFICATION_GATE_TEMPLATE.md` — how a maintainer enables the CI gate.

## Open items carried forward

- E041 / E042 grid artifacts still drift by 29–133 numeric differences (1-ulp sensitivity of
  an ill-conditioned tangency QP). This is documented in ledger E049; do **not** re-pin to
  hide it.
- The intended CI verification gate remains uncreated (maintainer action required).

## Provenance

This artifact supersedes `handoff_2026-11-19T23-33-52Z_INITIAL_TASK.md` only as the current
durable handoff. No earlier handoff content or golden/data baseline was altered.

## Procedure to leave the next handoff (repeat this pattern)

1. Create `handoff_<UTC timestamp>_INITIAL_TASK.md` at the repo root.
2. Copy it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, and
   `.kilo/handoff/`.
3. Repoint every generic pointer to it:
   `python3 scripts/repoint_handoff.py handoff_<UTC timestamp>_INITIAL_TASK.md`
   (`scripts/repair_broken_handoff.py` fixes any broken links).
4. Append a new `E<next>` entry to `ledger/RESEARCH_LEDGER.md` recording the timestamp,
   file name, SHA-256, verified HEAD, guards run, and constraints honored.
5. Re-run both golden guards and confirm `git status` shows only the new handoff artifacts,
   the ledger entry, and expected ignored files.
