# Agentic Work Session Handoff

**Timestamp**: 2026-11-25T06:21:24Z
**Session ID**: Initial handoff for next agentic work session
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments pre-registered with falsification expectations and promotion gates. **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

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

## Key Artifacts
- **Golden files**: `experiments/*.json` (canonical research artifacts)
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (validated strategies)
- **Data cache**: `data/` (gitignored except pinned vintages)
- **Verification reports**: `.verify_reports/` (gitignored)

## Baseline Integrity Rules
1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores them after
2. **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Golden baseline pinned** in `ledger/golden_baseline.json` — never re-pin without ledger entry
4. **Cache coverage enforced** — all `data.download()` calls must have pinned SHA-256 in `ledger/data_baseline.json`

## Current State
- Research phase complete (E001–E043)
- E042 (min-var confirmatory): PARTIAL
- E041 (market-neutral): REJECTED
- E025 (cointegration stat-arb): REJECTED
- All 26 committed drivers reproduce with 0 differences (extended verification 2026-11-23)

## Next Steps for New Session
1. Run `SEED=42 bash scripts/check.sh` to verify environment
2. Check `ledger/RESEARCH_LEDGER.md` for current dispositions
3. Review any open issues in `VERIFICATION_GATE_TEMPLATE.md` for CI setup
4. All verification commands are deterministic with `SEED=42`

---
*This handoff was created automatically at session start. Update as needed.*