# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T08:21:28Z
**Session Context:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Verification infrastructure hardened (golden baselines pinned, cache coverage enforced, optimizer determinism fixed per E049).

## Initial Task (Clear & Actionable)

**Goal:** Verify the repo is in a clean, reproducible state before any new work.

Run this first and confirm it passes before touching anything:

```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

`scripts/check.sh` runs: `py_compile` on changed files, golden-clean check vs HEAD, golden-baseline fingerprint check vs `ledger/golden_baseline.json`, portfolio-optimizer tests, convention robustness, and template validation.

## Current Known Blockers / Open Items

- **E041 drift (open):** Extended verification still reports E041 drifting (133 numeric diffs, down from 354). Root cause is 1-ulp sensitivity of an ill-conditioned tangency QP in `src/portfolio_opt.py`. Do **not** re-pin goldens to silence it. See `ledger/RESEARCH_LEDGER.md` E049.
- **Golden baseline integrity:** Never let verification overwrite `experiments/*.json`. Restore via `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` if interrupted/dirty.
- **Data coverage:** All `data.download()` inputs must be tracked and pinned in `ledger/data_baseline.json`; use `QUANT_RESEARCH_OFFLINE=1` in verification.

## Concrete Next Steps (in order)

1. Confirm `scripts/check.sh` passes clean.
2. If it fails on goldens, restore goldens, then re-run `scripts/check.sh`.
3. Triage E041 numerical stability: reproduce with `SEED=42 python3 run_all_verification.py --extended`, inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`, then profile `src/portfolio_opt.py` tangency path for conditioning/scaling without changing economic decisions.
4. Only after (1)-(3) are stable: consider deferred blend optimization (E015), pre-registered with gates/sensitivity.

## Verification Commands

- Fast integrity: `SEED=42 bash scripts/check.sh`
- Quick verification (restores goldens): `SEED=42 python3 run_all_verification.py`
- Extended (shows E041 drift): `SEED=42 python3 run_all_verification.py --extended`
- Recovery if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Guardrails

- Always use `SEED=42`.
- Never re-pin baselines as a side effect of verification runs.
- Never modify `experiments/*.json` without explicit justification + `scripts/check_golden_baseline.py --update`.
- Pre-register any new experiment before running; no goalpost moving.
- Cost model: tc=0.5bps + slippage=0.2bps, next-day open execution.

(End of file)
