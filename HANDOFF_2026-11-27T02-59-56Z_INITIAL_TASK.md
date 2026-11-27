# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-27T05:00:41Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project:** Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data (Research phase complete: E001–E043)

## Current State

- **Research phase complete** — surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Golden baseline** pinned in `ledger/golden_baseline.json` (SHA-256 fingerprints of `experiments/*.json`)
- **Data coverage** enforced via `scripts/check_data_coverage.py` against `ledger/data_baseline.json`
- **Verification suite** operational: `make check`, `make verify-quick`, `make verify-extended`, `make verify-full`

## Key Files to Know

| File | Purpose |
|------|---------|
| `AGENTS.md` | Project commands, conventions, reproducibility rules |
| `ledger/RESEARCH_LEDGER.md` | Experiment dispositions (E001–E050) |
| `ledger/golden_baseline.json` | SHA-256 pins for canonical artifacts |
| `scripts/check.sh` | Fast convention-robustness + template validation |
| `run_all_verification.py` | Full verification driver (quick/extended/full) |
| `src/batch_run.py`, `src/validate.py` | Core batch/validation entry points |

## Recent Verification Status (2026-11-23T05:17Z)

- **All 18 extended drivers reproduce with 0 differences** (numeric_tol=1e-4)
- E029 offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`)
- E030 reproduces with 0 differences since 2026-10-20 (16-ETF panel committed)
- E041/E042 bit-reproducible via E050 exact active-set enumeration fix (commit `72dc947`)

## Critical Rules (from AGENTS.md)

1. **Never leave verification half-finished** — snapshots in `.verify_snapshot/` with `ACTIVE.json` marker; recover with `--restore-only`
2. **Never commit verification output** — restore goldens before committing (`run_all_verification.py --restore-only` or `git checkout -- experiments/`)
3. **Do not re-pin goldens to silence tolerance violations** — only re-pin for deliberate code changes recorded in ledger first
4. **Cache coverage is invariant** — `scripts/check_data_coverage.py` enforces tracked + SHA-256 match for every download call site
5. **Optimizer determinism** — validated on problem constraints, not solver exit status (`tests/test_portfolio_opt.py`)

## Suggested Next Steps

- Run `SEED=42 bash scripts/check.sh` for fast convention check
- Run `SEED=42 python3 run_all_verification.py --extended` for full structural match
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategy dispositions

---

*This handoff was created automatically at session start. Update as needed.*