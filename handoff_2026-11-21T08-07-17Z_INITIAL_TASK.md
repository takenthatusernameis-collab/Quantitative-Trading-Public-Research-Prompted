# Agentic Work Session Handoff

**Created:** 2026-11-21T08:08:05Z
**Session:** Kilo (kilo-auto/free)
**Status:** READY FOR NEXT SESSION

## Working Directory

`/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Open Task

Continue independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## What to Do First

Run the fast convention-robustness check + template validation (seconds, offline):

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

This runs `py_compile` + `tests/test_portfolio_opt.py` + golden-baseline checks + data-coverage checks.

## Quick Reference Commands

```bash
# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Important Constraints

- Always use `SEED=42` (walk-forward + placebo RNG).
- `experiments/*.json` are committed golden artifacts; verification backs them up and restores them — never commit verification output.
- If interrupted mid-run: `SEED=42 python3 run_all_verification.py --restore-only`.
- Cache coverage is enforced: every `data.download()` call site must resolve to a committed, SHA-256-pinned cache file (see `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`).
- `QUANT_RESEARCH_OFFLINE=1` during verification — missing cache entries fail hard.
- No separate linter; run `python3 -m py_compile` on changed files.
- Do **not** re-pin goldens to silence optimizer drift (E041/E042 QP ill-conditioning; see ledger E049).
- CI workflow cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`.

## Open Items (from ledger)

- E041 drift: 133 numeric differences remain (1-ulp QP sensitivity); three structural differences fixed. Decision/REJECTED/gates unchanged. Do not re-pin.
- Optimizer determinism rule pinned by `tests/test_portfolio_opt.py`.

## Key Files

- `AGENTS.md` — conventions & commands (read before running suite)
- `ledger/RESEARCH_LEDGER.md` — validated strategies, E entries, open items
- `ledger/golden_baseline.json` — SHA-256 fingerprints of committed experiments
- `ledger/data_baseline.json` — pinned data cache fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh` — convention-robustness + template validation
- `scripts/check_goldens_clean.py` — working tree vs HEAD
- `scripts/check_golden_baseline.py` — working tree vs pinned fingerprints (`--update` to re-pin)
- `scripts/check_data_coverage.py` — cache coverage invariant (`--update` to add pins)
- `src/portfolio_opt.py` — optimizer validates on problem constraints, not exit status
- `tests/test_portfolio_opt.py` — determinism rule test
- `run_all_verification.py` — verification suite driver

## Last Known State

No uncommitted changes expected. Verify `git status` is clean before starting; if not, determine whether captured verification output needs restoring via `--restore-only`.
