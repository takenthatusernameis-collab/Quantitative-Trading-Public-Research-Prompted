# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T04:22:57Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline)
- **Data vintage:** 2026-10-12 (pinned in `data/vintages.json`), 2026-10-11 (committed for E026/E028/E029/E030/E034/E036/E037)
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`

## Verification Commands (SEED=42)

```bash
make check
make verify-quick
make verify-extended
make verify-full
make verify
```

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
2. **Golden baseline is pinned** in `ledger/golden_baseline.json` (SHA-256). Do not re-pin as side effect of verification.
3. **Data coverage is enforced** — `scripts/check_data_coverage.py` requires all cache files exist, tracked, and match `ledger/data_baseline.json`
4. **Optimizer determinism** — SLSQP status 8 is valid at constrained optimum; gating on it caused environment-dependent E042 (fixed by E050 exact active-set enumeration)
5. **CI gate cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`

## Initial Task

Default: await explicit user instructions. If acting autonomously:
1. Verify working-tree cleanliness against HEAD (`git status`).
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Last Verification Status

Run `SEED=42 python3 run_all_verification.py --extended` to verify current state.