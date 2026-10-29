# HANDOFF — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T20-41-12Z
**Handoff ID:** handoff-20261029T204112Z
**Status:** Durable initial task message for next agentic work session.

## Initial Task Message (START HERE)

> Repository baseline is verified and stable. **No new research is warranted at this time.**
> Your primary task is to verify stability by running the extended verification suite, confirm the pre-existing known drifts remain unchanged, and report results.
> **Do not modify goldens, weaken tolerances, or change any gate logic.**
> If interrupted during verification, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
> All constraints documented below still apply.

## What Was Verified (this session)

- `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (py_compile, imports, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, template validation, experiment-script imports).
- Working tree clean of tracked changes; only `__pycache__/*.pyc` mtime drift (unstaged, leave as-is).
- No `.verify_snapshot/` active; no stale verification output; `experiments/*.json` match HEAD and pinned `ledger/golden_baseline.json` fingerprints.
- No golden drift vs HEAD, no data-coverage issues.

## Precise Task

1. Run extended verification:
```bash
SEED=42 python3 run_all_verification.py --extended
```
2. Report:
- Overall pass/fail of extended suite
- Confirmation that E030 and E041 drifts match known pattern (counts/nature) with no new structural diffs
- Any anomalies (snapshot active, golden drift vs HEAD, data coverage issues)
- Final state recommendation (stable / needs attention)

**Expect pre-existing E030/E041 drift.** Do **not** weaken tolerances, skip drivers, or modify committed goldens.

## Known Pre-Existing Drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not re-pin.
- **E041/E042 sensitivity grids and full E042 confirmatory golden**: residual 1-ulp sensitivity in sandbox; no structural differences, no gate/decision affected. Do **NOT** re-pin — see ledger E049 and `HANDOFF_REPRO_CAVEAT.md`.

## Hard Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Never leave a verification run half-finished (suite backs up/restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template `.github/workflow-templates/verification-gate.yml`, instructions `VERIFICATION_GATE_TEMPLATE.md`).
- Do not commit `__pycache__/*.pyc` (leave unstaged).
- Do not re-pin goldens or data baselines unless explicit, documented need (committed golden is authoritative).

## Candidate Next Research (unstarted; only if explicitly requested)

- **Optimize TSM+DN blend weights and evaluate adding a diversifier (E050+)** — pre-register with gates/falsification in `ledger/RESEARCH_LEDGER.md` before running. Prerequisites exist. Not part of stability verification above.

## References

- `AGENTS.md` — quick start, baseline integrity, reproducibility, constraints
- `ledger/RESEARCH_LEDGER.md` — E001–E049, decisions, known drifts
- `HANDOFF_REPRO_CAVEAT.md` — reproducibility caveats
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
