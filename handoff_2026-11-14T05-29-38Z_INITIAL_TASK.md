# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-14T05:29:38Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
**Canonical artifacts**: `experiments/*.json` are the committed golden baselines.

## Quick Start Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended
```

## Key Integrity Notes

- Golden files (`experiments/*.json`) are overwritten during verification and restored afterward — never leave a run half-finished; use `run_all_verification.py --restore-only` to recover.
- `scripts/check_golden_baseline.py` compares artifacts to SHA-256 pinned in `ledger/golden_baseline.json`; re-pinning requires an explicit `--update`.
- Cache coverage is enforced (`ledger/data_baseline.json`); run offline with `QUANT_RESEARCH_OFFLINE=1`.
- Seed: always `SEED=42`.

## Known Drift Items (verification suite)

- E030: offline-reproducible since 2026-10-20 (pinned panel).
- E041: 133 numeric diffs (1-ulp ill-conditioned QP sensitivity, ledger E049) — **do not re-pin**.
- E029: fully offline-reproducible (fundamentals pinned in `data/fundamentals/`).

## Dependencies

```bash
pip install -r requirements.txt  # numpy, pandas, scipy, pyarrow, statsmodels, yfinance
```

## Next Session Guidance

1. Run `make check` first to verify baseline integrity.
2. Consult `ledger/RESEARCH_LEDGER.md` for gated/validated strategies before new work.
3. New experiments must be pre-registered with gates, falsification expectations, and a sensitivity grid.
4. Sensitivity grids are "reported, not gated" — promotion requires a dedicated pre-registered confirmatory run.
5. Record negative results honestly (REJECTED / PARTIAL) with evidence.

---
*This handoff was created automatically at session initialization (2026-11-14T05:29:38Z).*
