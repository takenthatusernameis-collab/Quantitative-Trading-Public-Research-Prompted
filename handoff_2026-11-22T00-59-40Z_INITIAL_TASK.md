# Handoff — Agentic Work Session

**Timestamp:** 2026-11-22T01:00:10Z
**Session ID:** (new session)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Research Phase:** Complete (E001–E043)
- **Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Current Baseline:** Golden artifacts in `experiments/*.json` are canonical and pinned to `ledger/golden_baseline.json`
- **Data Vintage:** 2026-10-12 (pinned in `data/vintages.json`); E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Quick Commands

```bash
# Fast convention check (offline, seconds)
SEED=42 bash scripts/check.sh
# or
make check

# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or
make verify-extended

# Full verification (~15 min, includes E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full
# or
make verify-full

# Restore goldens if verification was interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Invariants

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `--restore-only` or `git checkout -- experiments/`
2. **Golden baseline integrity** — `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` guard against accidental baseline replacement
3. **Cache coverage** — `scripts/check_data_coverage.py` enforces all driver data inputs are pinned; run with `--update` to re-pin
4. **Optimizer determinism** — SLSQP status 8 is valid at constrained optima; tangency QP is ill-conditioned (1-ulp drift expected on E041/E042 grid artifacts)

## Open Items (from Ledger)

- **E041**: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — do not re-pin
- **E042**: Grid artifacts drift 29-133 differences — do not re-pin
- **E030**: Now offline-reproducible (16-ETF panel committed), reproduces with 0 diffs
- **E029**: Offline-reproducible since 2026-10-20 (fundamentals pinned)

## Next Steps (Suggested)

- [ ] Run `make check` to verify baseline integrity
- [ ] Run `make verify-quick` to confirm reproducibility
- [ ] Review `ledger/RESEARCH_LEDGER.md` for surviving strategy documentation
- [ ] Consider confirmatory runs for any grid configs that cleared gates (requires pre-registration + placebo)

---

*This handoff was created automatically at session start. Update as work progresses.*