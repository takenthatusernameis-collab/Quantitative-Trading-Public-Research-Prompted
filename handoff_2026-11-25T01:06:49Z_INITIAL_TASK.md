# Handoff — Quantitative-Trading Research

**Session ended:** 2026-11-25T01:11:45Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Pending task for next session

None specified. The only request was to leave this timestamped handoff message. No code changes were requested or made.

## Useful commands

- `SEED=42 bash scripts/check.sh` — fast convention-robustness check + template validation
- `SEED=42 python3 run_all_verification.py --quick` — quick full verification (~8 min)
- `python3 -m py_compile <file>` — compile-check a changed Python file

## Notes

- `experiments/*.json` are canonical research artifacts; never commit verification output.
- If a verification run was interrupted, restore goldens with `SEED=42 python3 run_all_verification.py --restore-only`.
- Cache pins are enforced: `scripts/check_data_coverage.py` requires pinned cache entries under `data/`.
