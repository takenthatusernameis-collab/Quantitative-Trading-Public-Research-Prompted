# Handoff — 2026-11-09T14:24:19Z

## Session Context
- **Project**: Quantitative-Trading-Public-Research-Prompted
- **Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies documented in `ledger/RESEARCH_LEDGER.md`

## Key Commands
```bash
# Fast convention-robustness check (~seconds)
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

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or
make verify
```

## Critical Notes
1. **Golden artifacts in `experiments/*.json` are canonical** — verification overwrites and restores them. Never leave a verification run half-finished.
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Data caches**: Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029 fundamentals). `QUANT_RESEARCH_OFFLINE=1` enforced during verification.
4. **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — must be created manually via GitHub UI.
5. **Open items in ledger**: E041 optimizer drift (133 numeric diffs), E042 grid artifacts drift — do not re-pin to silence.

## Next Steps
- Run `make check` to verify baseline integrity before any changes
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Any new experiment requires pre-registration with falsification expectations