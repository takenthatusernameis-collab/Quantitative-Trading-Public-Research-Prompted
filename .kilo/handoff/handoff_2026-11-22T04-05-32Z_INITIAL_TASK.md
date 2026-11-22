# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-22T04-05-32Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Repo state at handoff:** clean working tree (`git status --porcelain` empty), branch `main`, HEAD `8f842dad` (chore(kilo): checkpoint agent session), in sync with `origin/main`. No interrupted verification run (`.verify_snapshot/` absent).

## Initial Task for the Next Session

**No new research task has been assigned.** Do not invent, start, or re-run research
work, and do not modify canonical artifacts or baselines, until the user gives an
explicit instruction.

The standing task for every session in this repository is:

1. Read this file and `AGENTS.md` in full — `AGENTS.md` is the source of truth for
   commands, conventions, and the baseline-integrity rules.
2. Confirm the baseline is intact before doing anything else:
   ```bash
   SEED=42 bash scripts/check.sh        # core canonical-artifact guards must pass
   git status --porcelain               # must be empty before you start
   ```
   Expected green lines from `scripts/check.sh`:
   - `ALL COMMITTED JSON ARTIFACTS PARSE OK`
   - `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`
   - `ALL <N> PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`
   - `ALL <N> PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED`
   If a golden mismatch appears, restore with
   `SEED=42 python3 run_all_verification.py --restore-only` (or
   `git checkout <commit> -- experiments/<file>` using the commit whose SHA-256
   matches `ledger/golden_baseline.json`). Never re-pin goldens as a side effect of
   running verification.
3. Wait for the user's specific task instructions before making any changes.
4. Only commit when the user explicitly asks. Never commit verification output.
5. After code changes, run `python3 -m py_compile` on each changed Python file.
6. Before finishing a session that made changes, leave a fresh timestamped durable
   handoff (this file's pattern) for the next session and repoint the generic
   pointers with `python3 scripts/repoint_handoff.py <new-handoff-filename>`.

## Environment Note (observed at this handoff)

- The core canonical-artifact guards listed above pass in this sandbox.
- `tests.test_data_coverage` reports errors **only** because `pandas` is not
  installed in this runtime (`ModuleNotFoundError: No module named 'pandas'`). This
  is an environment gap, not a repository or baseline regression. Install
  dependencies with `pip install -r requirements.txt` if you need to run the full
  suite. Do not "fix" this by editing tests or baselines.
- Running the checks rewrites tracked `__pycache__/*.pyc` bytecode; restore them
  (`git checkout -- '*.pyc'`) so the tree is clean before you hand off.

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
| `scripts/repoint_handoff.py` | Repoint generic handoff symlinks to a new file |
| `Makefile` | `check`, `verify`, `verify-quick`, `verify-extended`, `verify-full` targets |

## Safety / Constraints

- Never commit without an explicit user request.
- Never commit verification output (anything under `experiments/` produced by a
  re-run).
- Never move pre-registered goalposts post-hoc; sensitivity grids are
  "reported, not gated."
- Do not add code comments unless asked.
- Do not guess or generate URLs unless clearly helpful for programming.

## Handoff Provenance

- Supersedes `handoff_2026-11-22T04-03-28Z_INITIAL_TASK.md` (and all earlier
  `*_INITIAL_TASK.md` handoffs). This file is the authoritative initial-task
  message for the next session.
- Durable copies written to the repository root, `handoff/`, and `.kilo/handoff/`;
  generic pointer symlinks repointed via `scripts/repoint_handoff.py`.
- No verification, experiments, or baselines were modified while producing this
  handoff; the working tree was left clean.

---
*Generated at session handoff (2026-11-22T04-05-32Z).*