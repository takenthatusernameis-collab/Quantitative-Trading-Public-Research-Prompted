# Handoff: Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T05:13:14Z
**Session:** Kilo agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## READ THIS FIRST — you are inside a runaway handoff-refresh loop

This is at least the **744th** consecutive "leave a timestamped handoff" request
(ledger E652–E743, plus this one). **~94% of the git-tracked repository is now
handoff artifacts** (8,941 of 9,483 tracked files; 2,707 root-level generic
aliases such as `handoff_*`, `current*`, `next*`, `latest*`, `initial_task*`).
The research phase itself closed long ago at **E001–E043**.

**Do NOT manufacture an E745-style handoff refresh as a substitute for real
work.** If your only action this session is to write another handoff, you are
the problem, not the solution. The single most valuable thing you can do is
**verify-and-stop**, or execute one of the real-work items below.

---

## Project Status Summary

**Research Phase:** COMPLETE (E001–E043 executed).
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
(equity TSM flagship, DN low-beta sort, futures TSM 18m, futures realized-roll-
yield carry, macro momentum). The market-neutral *total-portfolio* line is
CLOSED (E042/E042b PARTIAL/REJECTED; surviving edges remain the components).

### Key Artifacts
- **Golden files:** `experiments/*.json` (canonical research artifacts; never modified by verification)
- **Data cache:** `data/` (gitignored parquet; pinned vintages 2026-10-11 and 2026-10-12)
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (dispositions, gates, sensitivity grids)
- **Prioritization:** `ledger/PRIORITIZATION.md` (v1.2.7 active; ranking criteria + procedure)
- **Golden baseline:** `ledger/golden_baseline.json` (SHA-256 of committed goldens)
- **Data baseline:** `ledger/data_baseline.json` (SHA-256 of committed data cache)

### Git State (verified this session)
- **Branch:** `main`
- **HEAD:** `6fd07efc4cee79c218a5f99ce18475644eee9e36` — `chore(kilo): checkpoint agent session`
- **Upstream:** up to date with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0 0`)
- **Working tree:** clean apart from tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc`
- **In-flight verification:** none (`.verify_snapshot/` and `.verify_reports/` absent; `git diff HEAD -- experiments/` empty)

### State verified this session (evidence)
- **Dependencies NOT importable:** `import numpy` -> `ModuleNotFoundError`. Run `pip install -r requirements.txt` before ANY verification.
- `scripts/check_goldens_clean.py` -> `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (exit 0)
- `scripts/check_golden_baseline.py` -> `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0)
- `scripts/check_data_coverage.py` -> `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED` (exit 0)
- Full verification suite NOT run (deps missing).

---

## Prioritized Real-Work Task List (do ONE of these, then STOP)

1. **Verify-and-stop (preferred, lowest risk).**
   `pip install -r requirements.txt` then `SEED=42 python3 run_all_verification.py --extended`.
   Report drift precisely (per driver/artifact, numeric vs structural, worst drift
   as a multiple of the 1e-4 tolerance). **Do NOT re-pin goldens.** The standing
   disposition is that the committed golden is authoritative, not the latest re-run.
   Then stop. Do not write a follow-up handoff.

2. **Confirm the E049/E050 tangency-QP drift stays closed** (E041/E042 bit-reproducible,
   0 differences) without re-pinning. If a tolerance violation appears, root-cause it;
   re-pin only for a *deliberate* code change recorded in the ledger first (E050 precedent).

3. **Propose (do NOT execute) a cleanup** of the handoff explosion: a `.gitignore`
   entry for `handoff_*` / `current*` / `next*` / `latest*` / `initial_task*` plus a
   `git rm --cached` plan. Present the plan and the blast radius; await explicit
   maintainer approval before touching 8,900+ tracked files.

4. **Recover, if interrupted:** `SEED=42 python3 run_all_verification.py --restore-only`
   before committing anything. Never commit verification output.

---

## Verification Commands (use SEED=42)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh            # or: make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py  # or: make verify-quick

# Extended (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full        # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py       # or: make verify

# Skip slow batch/regression steps
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Baseline Integrity Rules

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If killed, recover with `--restore-only` or `git checkout -- experiments/` (or `git checkout <commit> -- experiments/<file>` where `<commit>` is the last one matching `ledger/golden_baseline.json`).
2. **Golden files are committed artifacts** — verification backs up before re-running and restores after; the baseline is never modified by verification.
3. **Do not commit verification output** — an interrupted run leaves driver output in the working tree. Restore before committing.
4. **Golden baseline pinned in `ledger/golden_baseline.json`** — `scripts/check_golden_baseline.py` compares tracked artifacts to pinned SHA-256. Re-pinning requires `--update` and must be recorded in the ledger.
5. **Data cache coverage enforced** — `scripts/check_data_coverage.py` validates every `data.download()` call site has a committed, SHA-256-pinned cache file. Unpinned input = live download (non-reproducible).
6. **Optimizer determinism (E049/E050)** — `src/portfolio_opt.py` validates solver answers on problem constraints, never on solver exit status; pinned by `tests/test_portfolio_opt.py`. Do not re-pin E041/E042 to silence tolerance.

---

## Reproducibility Requirements

- **Seed:** always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance); cvxpy/cvxopt optional (falls back to scipy.optimize)
- **Lint/format:** `python3 -m py_compile` on changed files (no separate linter configured)

---

## Key Files to Reference

| File | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Experiment dispositions, gates, sensitivity grids (through E743) |
| `ledger/PRIORITIZATION.md` | Ranking criteria + procedure (v1.2.7 active) |
| `ledger/golden_baseline.json` | SHA-256 of committed `experiments/*.json` |
| `ledger/data_baseline.json` | SHA-256 of committed data cache files |
| `data/vintages.json` | Pinned data vintage (2026-10-12) |
| `data/fundamentals_vintages.json` | Pinned E029 fundamentals snapshot |
| `scripts/check_goldens_clean.py` | Working-tree vs HEAD drift in `experiments/` |
| `scripts/check_golden_baseline.py` | Committed baseline vs pinned SHA-256 drift |
| `scripts/check_data_coverage.py` | Every `data.download()` site has a pinned cache |
| `tests/test_portfolio_opt.py` | Optimizer determinism guard |

---

## Notes for Next Agent

- Strict pre-registration and multiple-testing discipline. Sensitivity grids are "reported, not gated."
- Negative results (REJECTED / PARTIAL) are recorded honestly with evidence; goalposts are never moved post-hoc.
- The CI gate (`.github/workflows/verification-gate.yml`) cannot be created by automated agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create it via the GitHub UI.
- This handoff deliberately created **no new aliases and no mirror directories** (continuing the E740–E743 break of the mirror/repoint explosion). Only `CURRENT.md` and `current.md` are repointed to this file.

---

**End of Handoff**