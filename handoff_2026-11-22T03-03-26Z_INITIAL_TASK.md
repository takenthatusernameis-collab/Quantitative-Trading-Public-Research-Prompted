# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-22T03:03:26Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Repo state at handoff:** clean working tree (0 modified/untracked paths), HEAD `df27edc2` (chore(kilo): checkpoint agent session), branch `main`.

## Initial Task Message (read this first)

> You are starting a fresh agentic work session in this repository. Orient
> yourself and confirm the canonical baselines are intact before doing anything
> else. The research phase is **closed** (E001–E043); surviving validated
> strategies are recorded in `ledger/RESEARCH_LEDGER.md`. **No task has been
> assigned yet — do not invent or start new research work.** Wait for the user's
> explicit instructions. When you finish, leave your own timestamped handoff
> using the procedure at the bottom of this file.

## Start-Here Checklist (in order)

1. **Orient.** Run `git log --oneline -3` and `git status --porcelain`. Read
   `AGENTS.md` and the tail of `ledger/RESEARCH_LEDGER.md`. Confirm
   `git rev-parse HEAD` matches the HEAD recorded above and that the tree is
   clean.
2. **Recover any interrupted verification.** If `.verify_snapshot/` exists or
   `experiments/*.json` differ from HEAD, run
   `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout <commit> -- experiments/<file>` using the commit whose
   SHA-256 matches `ledger/golden_baseline.json`) **before** anything else.
3. **Confirm the golden guards pass** (fast, offline):
   - `python3 scripts/check_goldens_clean.py` → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
4. **Provision dependencies if needed:** `pip install -r requirements.txt`.
5. **Run the fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`).
6. **Do the user's task, or stop.** Do not invent scope from this handoff.
7. **Leave your own handoff** at the end (see *Handoff Procedure*).

## Project State Summary

- **Research phase:** complete (E001–E043). Surviving validated strategies are
  documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are committed goldens. The
  verification suite overwrites them while re-running drivers and restores them
  afterwards — a run must never be left half-finished (repo-local
  `.verify_snapshot/` + `ACTIVE.json` marker make a killed run recoverable).
- **Known open items (do NOT "fix" by re-pinning):**
  - E041 / E042 grid artifacts still drift 29–133 numeric differences from an
    ill-conditioned tangency QP (1-ulp sensitivity; see ledger E049). Expected.
  - E030 and E041 are reported as drifting by the `--extended` drift report.
  - The CI gate (`.github/workflows/verification-gate.yml`) cannot be created by
    automated agents; a maintainer must add it via the GitHub UI from
    `.github/workflow-templates/verification-gate.yml`.
- **Data invariants:** all `data.download()` call sites must be committed and
  SHA-256-pinned in `ledger/data_baseline.json` (enforced by
  `scripts/check_data_coverage.py`); E029 fundamentals pinned in
  `data/fundamentals/` per `data/fundamentals_vintages.json`.

## Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only

# Individual experiment driver examples
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## Lint / Typecheck

- No separate linter or formatter is configured.
- Verification runs `py_compile` + reproducibility checks; use
  `python3 -m py_compile <changed files>` locally.

## Key Files

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Commands, conventions, baseline-integrity rules |
| `ledger/RESEARCH_LEDGER.md` | Experiment ledger, decisions, open items |
| `ledger/golden_baseline.json` | SHA-256 fingerprints of golden artifacts |
| `ledger/data_baseline.json` | SHA-256 fingerprints of pinned data caches |
| `data/vintages.json` | Pinned data vintage (2026-10-12) |
| `data/fundamentals_vintages.json` | Pinned E029 fundamentals snapshot |
| `Makefile` | `check`, `verify`, `verify-quick`, `verify-extended`, `verify-full` targets |
| `scripts/repoint_handoff.py`, `scripts/repair_broken_handoff.py` | Handoff alias upkeep |

## Safety / Constraints

- Never commit without an explicit user request.
- Never commit verification output (anything under `experiments/` produced by a
  re-run).
- Never move pre-registered goalposts post-hoc; sensitivity grids are
  "reported, not gated."
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- Do not add code comments unless asked.
- Do not guess or generate URLs unless clearly helpful for programming.

## Handoff Procedure (for the session that follows this one)

1. Write `handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md` at the repo root
   (`YYYY-MM-DDTHH-MM-SSZ`, colons replaced by hyphens).
2. Repoint the stable aliases:
   `python3 scripts/repoint_handoff.py handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md`,
   then `python3 scripts/repair_broken_handoff.py handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md`
   if needed.
3. Leave changes uncommitted unless the user explicitly asks.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-22T03-03-26Z_INITIAL_TASK.md`
  (repo root). Earlier handoff history is retained.
- This session created this durable handoff only. No code, experiments,
  baselines, or canonical artifacts were modified.

---
*Generated at session start (2026-11-22T03:03:26Z).*