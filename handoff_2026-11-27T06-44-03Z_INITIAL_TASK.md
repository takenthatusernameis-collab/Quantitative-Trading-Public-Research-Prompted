# Agentic Work Session Handoff

**Timestamp**: 2026-11-27T06:45:29Z
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Phase**: Research complete (E001–E043) — surviving strategies in `ledger/RESEARCH_LEDGER.md`

## Current State

- **Verification baseline**: `experiments/*.json` are canonical artifacts (pinned SHA-256 in `ledger/golden_baseline.json`)
- **Data vintage**: 2026-10-12 (pinned in `data/vintages.json`); 2026-10-11 committed for E026/E028/E029/E030/E034/E036/E037
- **E029 fundamentals**: Pinned offline in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Cache invariant**: All `data.download()` call sites must have committed, SHA-pinned cache files (`ledger/data_baseline.json`)

## Key Commands

```bash
# Convention robustness only (fast, offline)
SEED=42 make check
# or
SEED=42 python3 scripts/check.sh

# Quick verification (~8 min, 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 make verify-quick
# or
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min, +18 committed drivers, structural match)
SEED=42 make verify-extended
# or
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min, E042 n_sim=50 + 96-config sensitivity)
SEED=42 make verify-full
# or
SEED=42 python3 run_all_verification.py --full

# Restore goldens after interrupted run
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

## Critical Rules (from AGENTS.md)

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after; interrupted runs leave driver output in place of goldens
2. **Golden mismatch = fix before commit** — `scripts/check_goldens_clean.py` compares working tree to HEAD; `scripts/check_golden_baseline.py` compares to pinned SHA-256
3. **Do not re-pin to silence tolerance violations** — only re-pin for deliberate code changes recorded in ledger (E050 precedent)
4. **Offline reproducibility**: `QUANT_RESEARCH_OFFLINE=1` enforced in verification; missing cache = hard failure
5. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status (tested in `tests/test_portfolio_opt.py`)

## Recent Context

- E050 fix (commit `72dc947`): Exact KKT active-set enumeration for tangency solver → bit-reproducible E041/E042 (0 differences at 2026-11-23T05:17Z)
- E029/E030 offline-reproducible since 2026-10-20 (pinned data panels)
- Cache coverage invariant enforced 2026-10-20 (ledger E048)

## Next Session Suggestions

- Run `SEED=42 make check` to verify convention robustness
- If modifying drivers: run `SEED=42 make verify-quick` before committing
- Check `ledger/RESEARCH_LEDGER.md` for surviving strategy dispositions
- Any new data input: commit cache file + `python3 scripts/check_data_coverage.py --update`

---

*This handoff is durable — it persists in the repo for the next agentic session.*