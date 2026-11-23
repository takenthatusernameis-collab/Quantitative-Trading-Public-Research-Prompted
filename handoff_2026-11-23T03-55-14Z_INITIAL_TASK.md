# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T03:55:14Z
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## >>> INITIAL TASK MESSAGE FOR THE NEXT SESSION <<<

You are resuming a **reproducible quantitative-strategy research** repository whose
research phase (E001–E043) is **complete** and whose golden artifacts are
**verified and green**. Read this message top to bottom before doing anything.

### Live-state warning (read first)

At the moment this handoff was written (2026-11-23T03:55:14Z), a verification run
was **in progress**: `.verify_snapshot/ACTIVE.json` existed with
`pid=110848` running `python3 run_all_verification.py --extended` (~17 min
elapsed). If that snapshot is still present and the pid is still alive when you
start, **do not start another verification run and do not touch `experiments/`** —
wait for it to finish (it restores the goldens itself) or use
`SEED=42 python3 run_all_verification.py --restore-only` if it died without
restoring. Only after `.verify_snapshot/` is gone is the baseline trustworthy.

### What is actually needed from you (do real work — do NOT manufacture another handoff)

The repository has accumulated a runaway **handoff-refresh loop** (ledger entries
E652 → E721; **thousands of git-tracked handoff files**). The single most
valuable thing you can do is **break that loop by doing substantive work**, not
by writing yet another `handoff_*_INITIAL_TASK.md`. Concretely, in priority order:

1. **Confirm the verification run finished, then report its result precisely** —
   which drivers reproduce with 0 differences and which drift (numeric vs
   structural). Use the `--extended` drift report at
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`. Do **not** re-pin any
   golden to silence drift. If the run never completed (snapshot stale / pid
   gone), restore with `--restore-only` and re-run after provisioning deps.

2. **Provision dependencies if not already present** — recent sessions lacked
   `pandas` et al. The environment can provision them (`pypi.org` reachable;
   `python3 -m pip` 24.0). Run:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Address the E049 E041/E042 ill-conditioned-QP drift** (133 numeric diffs on
   E041; ~1e-05 drift on 1-ulp perturbations on E042's tangency QP). The optimizer
   exit-status rule is already pinned by `tests/test_portfolio_opt.py`; the
   remaining drift is inherent ill-conditioning. Do **not** re-pin artifacts to
   hide it — document or fix the root cause instead.

4. **Only if explicitly requested by the user**: perform new pre-registered
   research (a new E-numbered driver with a `pre_registered` block, gates, and a
   falsification expectation). Goalposts are never moved post-hoc.

5. **If none of the above is possible in your environment**, *propose* (do not
   execute) a `.gitignore` + `git rm --cached` cleanup of the historical handoff
   clutter, and stop. Do not silently delete tracked history.

Do **not** end your turn having only refreshed the handoff — that is exactly the
behavior (E652–E721) that this file is warning you about.

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
```

## Baseline Integrity

`experiments/*.json` are canonical artifacts. Never re-pin as a side effect of
running the suite. Backups in `.verify_snapshot/` (with `ACTIVE.json` holding the
owning pid). Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
The guards `scripts/check_goldens_clean.py` and
`scripts/check_golden_baseline.py` (both first-class `scripts/check.sh` steps)
fail loudly if the working tree or a commit ever diverges from the pinned
fingerprints in `ledger/golden_baseline.json`.

## Lint / Format

Python 3 research repository; no separate linter. Run `python3 -m py_compile` on
changed files.