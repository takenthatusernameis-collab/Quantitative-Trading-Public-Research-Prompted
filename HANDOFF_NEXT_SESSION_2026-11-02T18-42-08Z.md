# Agentic Handoff — Initial Task

**Created:** 2026-11-02T19:15:53Z
**Session:** new session, main agent (busy)
**Working tree:** clean (no uncommitted changes)
**Branch:** default / HEAD

## Project context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Recommended first action

Run the convention-robustness check + template validation (~seconds, offline):

```bash
SEED=42 bash scripts/check.sh
```

If that passes, proceed to a quick full verification (~8 min):

```bash
SEED=42 python3 run_all_verification.py
```

## Key constraints / warnings

- `experiments/*.json` are canonical research artifacts; verification re-runs drivers and restores them. Never leave a verification run half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do not commit verification output. Golden files must not be modified by a run; re-pinning requires `python3 scripts/check_golden_baseline.py --update` and explicit pinning.
- Cache coverage is enforced: run drivers with `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard. To add an input, commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.
- No separate linter; run `python3 -m py_compile` on changed Python files.

## Verification commands

- `make check` = convention robustness only
- `make verify` = verify-quick
- `make verify-extended` = extended (~21 min)
- `make verify-full` = full (~15 min)
