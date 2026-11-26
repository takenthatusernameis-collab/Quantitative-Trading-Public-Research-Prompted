# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T08:09:17Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `HANDOFF_2026-11-26T08-09-17Z_INITIAL_TASK.md` (repo root)

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State
- Branch: `main`
- HEAD: `01e684387801472233ca6f310a3b5279872ff7f6`
- Working tree: modified `src/__pycache__/cache_keys.cpython-312.pyc` (tracked build noise)

## Quick Commands
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 committed drivers vs goldens)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes
- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Golden files**: `experiments/*.json` are canonical artifacts — never commit verification output.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` if a verification run is interrupted.
- **Data**: Cached parquet in `data/` (gitignored except pinned 2026-10-12 and 2026-10-11 vintages; E029 fundamentals pinned in `data/fundamentals/`).
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification; unpinned input fails hard.
- **Dependencies**: NOT provisioned this session; run `pip install -r requirements.txt` first.
- **Optimizer determinism**: `src/portfolio_opt.py` validates solver answers on constraints, not solver exit status (ledger E049/E050; exact KKT active-set enumeration, commit `72dc947`).

## Initial Task
Default: await explicit user instructions. If acting autonomously:
1. Verify working-tree cleanliness against HEAD (`git status`).
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Last Verification Status
Not run in this session. Run `SEED=42 python3 run_all_verification.py --extended` to verify current state (numeric_tol=1e-4 vs goldens).
