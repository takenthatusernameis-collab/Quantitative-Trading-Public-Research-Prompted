# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T16:28:08Z
**Session ID**: Initial task message for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project State Summary

**Research Phase**: COMPLETE (E001–E043)
- Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- All experiments pre-registered with falsification expectations and promotion gates
- Branch: `main`

## Initial Task for Next Session

No explicit user task was provided in this session. Leave the workspace clean and ready, then verify baseline integrity:

1. `git status` — confirm working tree clean against HEAD (no half-finished verification output in `experiments/`).
2. `SEED=42 bash scripts/check.sh` — fast convention-robustness check + template validation (~seconds, offline).
3. If clean, `SEED=42 python3 run_all_verification.py --extended` — reproduce committed drivers and report any drift; do NOT re-pin goldens.

## Key Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full
```

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical research artifacts. Verification suite overwrites them during re-run and restores afterward. **Never leave a verification run half-finished** and never commit verification output over goldens.
2. **Recovery**: If interrupted, `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
3. **Baseline Protection**: `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires deliberate action and a ledger entry.
4. **Data Cache**: Cached parquet in `data/` (gitignored except pinned 2026-10-12/2026-10-11 vintages). E029 fundamentals pinned separately in `data/fundamentals/` per `data/fundamentals_vintages.json`.
5. **Offline Mode**: Verification runs with `QUANT_RESEARCH_OFFLINE=1` — missing cache entries fail hard.
6. **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).

## Convention

- **Seed**: Always `SEED=42` (walk-forward + placebo RNG)
- **Primary**: Close-to-close (v1.2.3); overnight decomposition reported alongside
- **Golden files**: `experiments/*.json` are authoritative; never re-pin as side effect of verification

---

*This handoff was created at session start for the next agentic work session. Update as needed during work.*