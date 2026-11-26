# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T00:31:54Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline)
- **Data vintage:** 2026-10-12 (pinned in `data/vintages.json`), 2026-10-11 (committed for E026/E028/E029/E030/E034/E036/E037)
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Verification Commands (SEED=42)

```bash
# Fast convention check (~seconds)
make check

# Quick full verification (~8 min)
make verify-quick

# Extended verification (~21 min)
make verify-extended

# Full verification (~15 min)
make verify-full

# Convention robustness only
make verify
```

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Golden baseline is pinned** in `ledger/golden_baseline.json` (SHA-256). Do not re-pin as side effect of verification.
3. **Data coverage is enforced** — `scripts/check_data_coverage.py` requires all cache files exist, tracked, and match `ledger/data_baseline.json`
4. **Optimizer determinism** — SLSQP status 8 is valid at constrained optimum; gating on it caused environment-dependent E042 (fixed by E050 exact active-set enumeration)
5. **CI gate cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`

## Active/Recent Issues

- E041/E042 ill-conditioned-QP drift resolved by E050 fix (exact KKT active-set, commit `72dc947`) — now bit-reproducible (0 differences)
- E029 offline-reproducible since 2026-10-20 (fundamentals pinned)
- E030 offline-reproducible since 2026-10-20 (16-ETF panel committed)
- All 18 extended drivers reproduce with 0 differences (2026-11-23T05:17Z measurement)

## Next Steps (if any)

- Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
- Run `make check` to verify working tree integrity before any changes
- Any new experiment requires pre-registration with falsification expectations