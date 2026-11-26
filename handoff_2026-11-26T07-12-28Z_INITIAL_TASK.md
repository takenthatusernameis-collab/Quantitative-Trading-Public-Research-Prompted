# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T07:12:28Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline)
- **Data vintage:** 2026-10-12 (pinned in `data/vintages.json`), 2026-10-11 (committed for E026/E028/E029/E030/E034/E036/E037)
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- **HEAD:** `afdf31b1` (`chore(kilo): checkpoint agent session`)

## Initial Task

Default: await explicit user instructions. If acting autonomously:

1. Verify working-tree cleanliness against HEAD (`git status`).
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check: goldens clean, golden baseline, data coverage, optimizer determinism).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and report any drift; do NOT re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Last Verification Status

Not run in this session. Run `SEED=42 python3 run_all_verification.py --extended` to verify current state. The extended suite re-executes the committed drivers and compares against goldens with `numeric_tol=1e-4`.
