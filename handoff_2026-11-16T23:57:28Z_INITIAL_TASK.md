# Agentic Work Session Handoff

**Timestamp**: 2026-11-16T23:58:25Z
**Session ID**: Initial handoff created by Kilo assistant
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Commands
```bash
# Fast convention-robustness check + template validation
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
```

## Key Files
- `ledger/RESEARCH_LEDGER.md` - Validated strategies and experiment outcomes
- `ledger/golden_baseline.json` - SHA-256 pinned baseline artifacts
- `ledger/data_baseline.json` - SHA-256 pinned data cache entries
- `experiments/*.json` - Canonical research artifacts (golden files)
- `scripts/check.sh` - Convention robustness + golden integrity checks
- `run_all_verification.py` - Full verification suite driver

## Verification Suite Notes
- **Golden files**: `experiments/*.json` are backed up to `.verify_snapshot/` during verification and restored after. Never leave a verification run half-finished.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- **Cache coverage**: Enforced invariant - all `data.download()` calls must have pinned cache files matching `ledger/data_baseline.json`
- **Seed**: Always use `SEED=42` for reproducibility

## Current State
- Research phase complete (E001–E043)
- No active verification run in progress
- Working tree clean relative to HEAD (verify with `scripts/check.sh`)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment integrity
2. Check `ledger/RESEARCH_LEDGER.md` for current strategy dispositions
3. Run verification suite as needed: `make verify-quick` / `make verify-extended` / `make verify-full`
4. Any new experiments must follow pre-registration protocol with falsification expectations