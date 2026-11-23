# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-23T03:57:38Z
**Workspace**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD**: `8633ee760071d5b27cae06841baf1eda24d565c3` on `main`, equal to `origin/main` (`0 0` ahead/behind)
**Repository**: Reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase E001–E043 is complete; surviving validated strategies are recorded in `ledger/RESEARCH_LEDGER.md`.

## >>> INITIAL TASK MESSAGE FOR THE NEXT SESSION <<<

### Read this first: live-state warning

At the timestamp above, an extended verification run was **still active**:

- `python3 run_all_verification.py --extended` was running as pid `110848` (parent `110847`).
- `.verify_snapshot/ACTIVE.json` existed; it is gitignored and lists the canonical `experiments/*.json` files temporarily owned by the verification run.
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` therefore reported: `verification run in progress (pid 110848); the golden artifacts are temporarily modified by design` and skipped fingerprint comparison.
- `git diff --name-only -- experiments` was empty at handoff time, but this is a moving state while the run is alive.

**Do not start another verification run while pid `110848` is alive.** Do not touch, re-pin, restore, or commit anything under `experiments/` until the active run exits and restores the goldens itself. If the process is gone but `.verify_snapshot/` remains, recover before doing anything else:

```bash
SEED=42 python3 run_all_verification.py --restore-only
```

Only after `.verify_snapshot/` is gone and the golden guards pass should the working tree be considered trustworthy.

### Required first actions

1. Check the live process and snapshot state:
   ```bash
   ps -p 110848 -o pid=,ppid=,etime=,stat=,cmd=
   ls -la .verify_snapshot
   git status --short
   ```
2. If the process is still alive, wait for it to finish; do not poll aggressively and do not start parallel verification.
3. When the snapshot is gone, run the fast integrity gate:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
4. If the extended report exists, read and summarize it:
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`
5. Do not re-pin golden artifacts to silence drift. The committed goldens in `ledger/golden_baseline.json` are authoritative; replacing a golden requires a deliberate, user-visible diff.

### Most valuable substantive work after recovery

1. **Report the extended verification outcome precisely**: which drivers reproduce with zero differences, which have numeric drift, and whether any structural/string differences appeared. Cite per-driver counts and compare against the expectations documented in `AGENTS.md` and the ledger.
2. **Address or characterize the E041/E042 ill-conditioned-QP drift** without hiding it. `src/portfolio_opt.py` already validates answers on problem constraints rather than solver exit status, and `tests/test_portfolio_opt.py` pins that rule. The remaining drift is optimizer/numerical sensitivity; do not re-pin artifacts merely to silence it.
3. **Only if explicitly requested by the user**, perform new pre-registered research: add an E-numbered driver with a `pre_registered` block, gates, falsification expectation, placebo plan, and sensitivity grid. Goalposts must never move post-hoc.
4. **Break the handoff-refresh loop**. The repository contains thousands of tracked handoff files and ledger evidence of repeated handoff-only work. Do not write another handoff as the terminal action unless the user explicitly asks for one. Prefer substantive verification, diagnosis, tests, or research.

### Forbidden shortcuts

- Do not commit verification output.
- Do not modify `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of running tests.
- Do not delete tracked history or mass-remove handoff files without explicit user approval.
- Do not claim the suite passed unless the guards and driver comparisons actually passed.
- Do not leave `.verify_snapshot/` abandoned; recover interrupted runs with `--restore-only`.

## Current working-tree state at handoff time

- Branch `main` is synchronized with `origin/main`.
- The only ordinary modified files shown by `git status` were pre-existing tracked `__pycache__/*.pyc` files under `scripts/`, `src/`, and `tests/`. Treat those as build artifacts; do not commit them unless explicitly instructed.
- This handoff session did not start verification, did not mutate `experiments/`, and did not commit anything.

## Project commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick verification (~8 minutes)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 minutes; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended

# Full verification (E042 n_sim=50 + sensitivity grid)
SEED=42 python3 run_all_verification.py --full

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Baseline and reproducibility rules

- `experiments/*.json` are canonical committed artifacts. The verification suite backs them up in `.verify_snapshot/`, re-runs drivers, and restores them afterward.
- `scripts/check_goldens_clean.py` compares the working tree to `HEAD`; `scripts/check_golden_baseline.py` compares artifacts to the SHA-256 fingerprints in `ledger/golden_baseline.json`.
- Data inputs are pinned by `ledger/data_baseline.json` and checked by `scripts/check_data_coverage.py`; the suite runs drivers offline with `QUANT_RESEARCH_OFFLINE=1`.
- Use `SEED=42` for every reproducibility check.
- Close-to-close is the primary convention; overnight decomposition is reported alongside for strategies.
- Dependencies are `pip install -r requirements.txt`; `cvxpy`/`cvxopt` are optional and the optimizer falls back to `scipy.optimize`.

## Open research/engineering items

- E041/E042 grid artifacts can drift because the tangency QP is ill-conditioned. Do not re-pin to silence this; diagnose or document the numerical behavior.
- E030 and E029 have been offline-reproducible since 2026-10-20 after their inputs were pinned.
- The known remaining extended-drift hotspot is E041; E030 was previously a drifter but is now expected to reproduce with zero differences.
- New research must be pre-registered and must include negative or failed results honestly.

## Handoff convention

This timestamped file is the durable initial task message. Generic stable aliases such as `handoff_CURRENT.md`, `handoff_LATEST.md`, `handoff_NEXT.md`, and `handoff_INITIAL_TASK.md` were repointed to this file with `scripts/repoint_handoff.py`. Historical timestamped handoffs are left untouched.