# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T05:03:38Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline, SHA-256 pinned in `ledger/golden_baseline.json`)
- **Data vintage:** 2026-10-12 (pinned in `data/vintages.json`); 2026-10-11 committed for E026/E028/E029/E030/E034/E036/E037
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **Working tree:** Clean at HEAD (`c76644bc`); `experiments/` matches HEAD (no half-finished verification); no `.verify_snapshot/` present.

## Verification Commands (SEED=42)

```bash
make check            # fast convention-robustness + template validation (~seconds, offline)
make verify-quick     # ~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2
make verify-extended  # ~21 min; quick + 18 more committed drivers, structural match
make verify-full      # ~15 min; E042 n_sim=50 + 96-config sensitivity grid
make verify           # convention robustness only (reads JSONs, no writes)
```

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If HEAD already carries a captured run, restore the pinned artifact with `git checkout <commit> -- experiments/<file>` where `<commit>` matches `ledger/golden_baseline.json`.
2. **Golden baseline is pinned** in `ledger/golden_baseline.json` (SHA-256). Do not re-pin as a side effect of verification; re-pin only for a deliberate, ledger-recorded code change (E050 precedent).
3. **Data coverage is enforced** — `scripts/check_data_coverage.py` requires every cache file exist, be git-tracked, and match `ledger/data_baseline.json`. Run drivers with `QUANT_RESEARCH_OFFLINE=1`.
4. **Optimizer determinism** — SLSQP status 8 is valid at a constrained optimum; gating on it caused environment-dependent E042 (fixed by E050 exact active-set enumeration in `src/portfolio_opt.py`).
5. **CI gate cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.
6. **Do not commit verification output** — restore goldens before committing (`--restore-only`).

## Initial Task

Default: await explicit user instructions. If acting autonomously:
1. Confirm working-tree cleanliness against HEAD (`git status`); confirm no half-finished verification snapshot (`.verify_snapshot/ACTIVE.json`).
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Last Verification Status

Run `SEED=42 python3 run_all_verification.py --extended` to verify current state. Prior measurement (2026-11-23T05:17Z, numpy 2.5.4, scipy 1.18.1): all 18 extended drivers reproduce with 0 differences.