# Agentic Work Session Handoff

**Timestamp**: 2026-11-26T15:14:49Z
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase**: Research complete (E001–E043) — surviving strategies in `ledger/RESEARCH_LEDGER.md`

## Current State

- All 43 experiments pre-registered with falsification expectations
- Verification suite operational: `make check`, `make verify`, `make verify-full`
- Golden artifacts in `experiments/*.json` (canonical baseline)
- Data cached in `data/` (pinned vintages: 2026-10-11, 2026-10-12)
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Key Commands

```bash
# Fast convention check (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
```

## Critical Integrity Notes

- **Never leave verification half-finished**: golden artifacts in `experiments/` are overwritten during run and restored after. Use `--restore-only` to recover if interrupted.
- **Baseline protection**: `scripts/check_golden_baseline.py` compares `experiments/` against SHA-256 fingerprints in `ledger/golden_baseline.json`. Re-pinning requires deliberate ledger entry.
- **Cache coverage enforced**: `scripts/check_data_coverage.py` validates every `data.download()` call site — unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer determinism**: Tangency QP uses exact KKT active-set enumeration (E050 fix, commit `72dc947`) — bit-reproducible across environments.

## Next Session Suggestions

1. Run `make check` to verify working tree integrity
2. Run `make verify-quick` to confirm reproducibility baseline
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategy dispositions
4. Any new experiments must follow pre-registration protocol with falsification expectations

---
*This handoff is durable across sessions. Update timestamp on each new session start.*