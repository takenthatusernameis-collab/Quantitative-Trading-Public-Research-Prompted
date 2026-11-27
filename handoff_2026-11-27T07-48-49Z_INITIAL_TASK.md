# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-27T07:48:49Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status**: Research phase complete (E001–E043). No verification run in progress; no `.verify_snapshot/` present.

## Initial Task for the Next Session

1. Confirm a clean baseline before doing anything else:
   ```bash
   SEED=42 bash scripts/check.sh        # fast convention-robustness + golden-integrity guards
   ```
   This runs `check_goldens_clean.py` and `check_golden_baseline.py`. If it reports a
   golden mismatch, **fix it before committing** — do not commit verification output.
2. If the tree looks dirty, recover the golden artifacts first:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # or, if HEAD already carries a captured run, restore the pinned artifact:
   #   git checkout <commit> -- experiments/<file>   (commit whose SHA-256 matches ledger/golden_baseline.json)
   ```
3. Then run the appropriate verification tier (see below) and confirm 0 differences.
4. Only after a green check, proceed with the actual research/engineering task of the session.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full
```

## Key Notes for Next Session

- **Golden artifacts**: `experiments/*.json` are the canonical research artifacts. The
  verification suite backs them up to `.verify_snapshot/` (gitignored, pid-tracked) before
  re-running and restores them afterward. Never leave a run half-finished.
- **Never commit verification output** — restore goldens before committing. Re-pinning a
  golden (`scripts/check_golden_baseline.py --update`) is only for a deliberate code change
  recorded in the ledger first (see the E050 precedent).
- **Seed**: Always use `SEED=42` for reproducibility (walk-forward + placebo RNG).
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 / 2026-10-11
  vintages). E029 fundamentals pinned in `data/fundamentals/`. Cache hit is calendar-independent.
  The suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`; a missing cache entry fails hard.
- **Optimizer determinism (ledger E049/E050)**: `src/portfolio_opt.py` validates on the
  problem's constraints, not the solver exit status. E041/E042 are bit-reproducible under the
  E050 exact active-set tangency solver. Do not re-pin to silence tolerance violations.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout -- experiments/`).
- **Working tree note (2026-11-27T07:48:49Z)**: only tracked `__pycache__/*.pyc` files show as
  modified; there are no pending source/artifact changes. These are build artifacts and are not
  part of any research result.

## Recent Context

The E050 fix (exact KKT active-set enumeration as the primary tangency solver, commit `72dc947`)
made the E041/E042 grid artifacts bit-reproducible across environments (0 differences at the
2026-11-23T05:17Z measurement, numpy 2.5.4 / scipy 1.18.1). All 18 extended drivers reproduce
with 0 differences. E029 and E030 goldens were deliberately re-pinned to committed offline
snapshots (ledger E045/E048).

---

*This handoff was created automatically for the next agentic work session.*