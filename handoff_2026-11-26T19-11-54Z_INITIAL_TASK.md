# Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-26T19:11:54Z
**Durable artifact:** `handoff_2026-11-26T19-11-54Z_INITIAL_TASK.md` (repo root)
**Supersedes:** `handoff_2026-11-26T18-14-44Z_INITIAL_TASK.md`

## Initial task (next agentic session)

Run the verify-and-stop backlog, then stop. Do not manufacture more refreshes.

1. Provision deps: `pip install -r requirements.txt` (numpy, pandas, scipy,
   pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
2. Fast guard: `SEED=42 bash scripts/check.sh` (offline; ~seconds).
   - Pure-Python guards must PASS: goldens clean, 107 pinned goldens match
     baseline, 35 pinned data inputs present/tracked/unchanged.
3. Extended verification: `SEED=42 python3 run_all_verification.py --extended`
   (~21 min). Re-executes 18 committed drivers vs committed goldens
   (numeric_tol=1e-4, structural match). Report any drift; do NOT re-pin
   goldens to silence a tolerance violation (none should remain after E050).
4. Confirm the E049/E050 tangency-QP drift stays closed (E041/E042 bit-reproducible
   since commit `72dc947`; exact KKT active-set enumeration).
5. Propose (do NOT execute) a `.gitignore` + `git rm --cached` cleanup of the
   ~8,375 alias/handoff alias files.

**Seed:** always `SEED=42` (walk-forward + placebo RNG).
**Golden files:** `experiments/*.json` are canonical — never commit verification
output over them. If interrupted, recover with
`SEED=42 python3 run_all_verification.py --restore-only` (or
`git checkout <pinned-commit> -- experiments/<file>`).
**No separate linter:** run `python3 -m py_compile` on changed files.
**Never commit unless explicitly asked.**

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving
validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
Close-to-close is the v1.2.3 primary convention; overnight decomposition
reported alongside every strategy.
Verification suite runs every driver with `QUANT_RESEARCH_OFFLINE=1`; an
unpinned input fails hard instead of silently downloading.

## Git state

- Branch: `main`; HEAD `ad21665c` == `origin/main` (`0 0`).
- Working tree clean apart from tracked build noise
  `src/__pycache__/cache_keys.cpython-312.pyc` (safe to `git restore`).
- `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and
  `.verify_reports/` absent.

## Quick commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention-robustness + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 more drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Prior handoffs

Previous durable artifact: `handoff_2026-11-26T18-14-44Z_INITIAL_TASK.md`
(superseded by this one). Index: `.handoff.md`. Latest pointer: `current`.
