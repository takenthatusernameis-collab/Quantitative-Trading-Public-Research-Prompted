# Next Task Handoff (prepared 2026-10-20, E047)

## Repository state

The research phase (E001–E046) is complete. The repository is clean and
fully verified. This session (E047) found and fixed one documentation
defect; no code, golden, gate, or decision was changed.

## What this session did

Re-measured the E041/E042 reproducibility claims in isolated copies of the
repository (so the canonical goldens could not be captured mid-run) and
found that `README.md` carried a retracted caveat that contradicted itself:

- README:1024-1042 asserted that **both** `run_e041.py` and
  `run_e042.py --n-sim 50` "do **not** reproduce their committed goldens
  byte-for-byte".
- README:943-955 asserted that `run_e042.py --n-sim 50` reproduces **both**
  E042 goldens **byte-for-byte (0 diffs)**.

E044 (2026-10-19) had retracted the caveat for E042 in the *ledger* but
never updated the README paragraph, leaving two self-contradictory statements
in the published documentation.

### Evidence (measured this session, SEED=42, pinned deps + 2026-10-12 vintage)

- **E042**: `run_e042.py --n-sim 50` -> `e042_minvar_market_neutral.json` and
  `e042_sensitivity_grid.json` both **0 diffs** (including the full 96-config
  grid). E042 is **not** environment-sensitive.
- **E041**: `run_e041.py` -> `e041_market_neutral_portfolio.json` **7602
  numeric + 3 structural** diffs, `e041_sensitivity_grid.json` **151 numeric,
  0 structural**. The 3 structural diffs are the already-documented 8 -> 7
  market-neutral count, the "8 of 96" -> "7 of 96" note, and `top_configs`
  length 8 -> 7. Gate decision (REJECTED 3/5, G3 fails) unchanged.

### Changes made (documentation only)

- `README.md`: rewrote the E041-only caveat with measured diff counts; stated
  explicitly that E042 is not in this class; updated the E041 grid paragraph
  to quote the re-measured **7/96** (with the 8 -> 7 drift noted) instead of
  the committed **8/96**.
- `ledger/RESEARCH_LEDGER.md`: new **E047** entry.
- New `HANDOFF_SESSION_2026-10-20.md` (this repo's session handoff).

## Task for the next agent

**None outstanding.** The research phase is complete and the repository is
clean and fully verified (`SEED=42 bash scripts/check.sh` -> ALL CHECKS
PASSED; `git status` clean except the two documentation files from E047).

The only remaining durable action is the maintainer-gated CI workflow
creation (`.github/workflow-templates/verification-gate.yml` -> the GitHub
UI), which is outside agent scope per AGENTS.md.

If a bounded in-session task is desired, the remaining environment-sensitive
drivers are E030 and E041 — both are documented as reporting-only with
unchanged decisions, and no further work is warranted unless a maintainer
re-pins them deliberately.

## Constraints (unchanged)

- `SEED=42`, pinned 2026-10-12 price-cache vintage + pinned 2026-10-12
  fundamentals snapshot.
- No committed-golden modification unless it is a deliberate re-pin
  (`python3 scripts/check_golden_baseline.py --update` puts the replacement
  in the diff); no tolerance/driver/skip change; no goalpost moved.
- Honor crash-safety snapshot/restore (`python3 run_all_verification.py
  --restore-only`); never leave a verification run half-finished.
- Run slow drivers in isolated copies, not in the repository itself — the
  drivers overwrite `experiments/*.json`, and a checkpoint commit that
  captures verification output silently replaces the canonical baseline.
- Follow repo policy: the golden is authoritative; re-pinning only
  deliberately with justification.