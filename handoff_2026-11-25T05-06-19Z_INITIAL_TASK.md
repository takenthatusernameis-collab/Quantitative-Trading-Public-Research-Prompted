# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T05:06:19Z
**Session ID**: Initial handoff for next agentic session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Key Commands for Next Session

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

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

# Individual experiment commands
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py --universe large_liquid
SEED=42 python3 experiments/run_e025.py    # cointegration stat-arb (REJECTED)
SEED=42 python3 experiments/run_e041.py    # market-neutral portfolio (REJECTED)
SEED=42 python3 experiments/run_e042.py --n-sim 50  # min-var confirmatory (PARTIAL)
```

## Important Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG)
- **Golden files**: `experiments/*.json` are canonical artifacts - never commit verification output. `run_all_verification.py` backs up/restores them
- **Recovery**: If verification interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Baseline integrity**: `scripts/check_goldens_clean.py` fails if a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending. `scripts/check_golden_baseline.py` compares artifacts against SHA-256 pinned in `ledger/golden_baseline.json`
- **Data coverage**: `scripts/check_data_coverage.py` resolves every `data.download()` call site and requires pinned SHA-256 cache files. `QUANT_RESEARCH_OFFLINE=1` makes missing cache fail hard
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance)
- **Lint**: No separate linter; run `python3 -m py_compile` on changed files

## Current State

- Research phase complete (E001–E043); all experiments pre-registered with falsification expectations and gates
- `AGENTS.md` holds full project conventions and commands
- `experiments/` directory contains committed golden artifacts (not listed above)
- Verification suite validates reproducibility across environments
- Optimizer determinism pinned: `src/portfolio_opt.py` validates solver answers on problem constraints, never solver exit status (ledger E049/E050)

## Next Session Task

Run the verification suite to confirm reproducibility, starting with the fast check:

```
SEED=42 bash scripts/check.sh
```

If it passes, proceed to `make verify-quick`. Investigate any failures before committing. Do not commit verification output.
