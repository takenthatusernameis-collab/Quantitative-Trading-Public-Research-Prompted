# Handoff — Timestamped clear initial task for next agentic session

Timestamp (UTC): 2026-10-28T17:14:29Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: ae9d05c chore(kilo): checkpoint agent session
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state (verified this session)

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Baseline is clean and committed.** Verified this session:
  - `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED (py_compile, JSON parse, goldens match HEAD, golden baseline pin, data coverage, experiment imports, portfolio_opt tests).
  - `SEED=42 python3 scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH.
  - `SEED=42 python3 scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS PRESENT, TRACKED, UNCHANGED.
  - `python3 -m unittest tests.test_portfolio_opt` → 8 tests OK.
- Working tree clean of tracked changes. Only gitignored `__pycache__/*.pyc` show as modified (they are tracked on disk but ignored; not a baseline concern — do not commit unless intentionally regenerated).
- No `.verify_snapshot/` — nothing to recover.

## Open items (unchanged, do not re-pin to silence)

- **E041 numeric drift (~133 diffs)** from the ill-conditioned tangency QP in `src/portfolio_opt.py` (1-ulp sensitivity of SLSQP on `min y'Sy s.t. mu'y = 1, y >= 0, |B'y| <= c 1'y`). E041 decision REJECTED 3/5 is unchanged. Do NOT re-pin.
- **E042-lead** solver fix in place (ledger E049): the optimizer now validates answers on the problem's constraints, never on the solver's exit status. The tangency QP itself remains ill-conditioned — that residual drift is documented and handed off, not fixed.
- **E042 primary** (`run_e042.py --n-sim 50`) reproduces both goldens byte-for-byte (0 diffs) under the pinned 2026-10-12 cache vintage and `SEED=42`.

## Clear initial task for next session

Execute in order. Treat failures as blockers to fix before proceeding.

### 1) Confirm clean baseline (already passing, re-verify)
```bash
SEED=42 bash scripts/check.sh
```

### 2) Run quick verification (~8-10 min; use a long timeout or background)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted (SIGKILL/OOM/timeout), recover before anything else:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```

### 3) Optional extended verification
```bash
SEED=42 python3 run_all_verification.py --extended
```
Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). E041/E030 may show bounded numeric drift; structural changes are not acceptable. Do not re-pin.

### 4) Review open items before making changes
- Read `ledger/RESEARCH_LEDGER.md` (focus E049, E041, E048/E042-lead, E045/E046/E047/E048 drift dispositions).
- Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` before any intentional re-pinning.

## Constraints / reminders (do not skip)

- Always use `SEED=42`.
- Never leave a verification run half-finished; if unsure, run `--restore-only`.
- Never re-pin goldens as a side effect of running verification. Re-pinning is deliberate (`python3 scripts/check_golden_baseline.py --update`) and must be recorded in the ledger.
- If `scripts/check.sh` reports a golden mismatch, fix before committing — recover from the pinned commit (`git checkout <commit> -- experiments/<file>`), never by re-pinning.
- Data: pinned vintages in `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Missing caches fail under offline verification (`QUANT_RESEARCH_OFFLINE=1`).
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml` (maintainer creates via GitHub UI). Local equivalents: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`.
- Follow `AGENTS.md` conventions (pre-registration, multiple-testing discipline, negative results recorded honestly).
- Convention robustness: close-to-close primary; overnight decomposition reported alongside.
- `__pycache__/*.pyc` files are tracked and show as modified on clean checkout — not a baseline concern; do not commit unless intentionally regenerated.
- Environment: dependencies installed at `/home/runner/work/_temp/kilo-home/.local`. Fresh session may need `pip install -r requirements.txt` again. `pytest` is not installed; use `python3 -m unittest tests.test_portfolio_opt`.

## Suggested first commands (ready to run)
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

## Handoff notes
- Previous handoff: `HANDOFF_NEXT_SESSION_2026-10-28T17-10-00Z.md`. This file supersedes as the timestamped initial task message for the next session.
- Recovery procedure used this session is the canonical one in AGENTS.md: stale snapshot → `--restore-only` → if artifacts still mismatch the pin, `git checkout <pinned-commit> -- experiments/<file>` → commit the recovery.

(End of file — total 98 lines)