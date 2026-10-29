# Handoff for Next Agentic Work Session

**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Session Context:** Research phase complete (E001–E043). Verification infrastructure hardened. Repo working tree clean at c25fbea. No live verification snapshot (.verify_snapshot/ absent). Durable handoff for next session.

## Initial Task (Clear & Actionable)

**Goal:** Confirm the repo is in a clean, reproducible state before any new work.

Run this first and confirm it passes before touching anything:

```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

`scripts/check.sh` runs: `py_compile` on changed files, golden-clean check vs HEAD, golden-baseline fingerprint check vs `ledger/golden_baseline.json`, portfolio-optimizer tests, convention robustness, and template validation.

## Current Known Blockers / Open Items

- **E041 drift (open):** Extended verification still reports E041 drifting (~133 numeric diffs, down from 354). Root cause is 1-ulp sensitivity of an ill-conditioned tangency QP in `src/portfolio_opt.py`. Do **not** re-pin goldens to silence it. See `ledger/RESEARCH_LEDGER.md` E049.
- **E042 drift (open):** Extended verification reports E042 drifting (~29 numeric diffs) due to the same ill-conditioned tangency/min-var QP sensitivity. Do **not** re-pin goldens to silence it. See `ledger/RESEARCH_LEDGER.md` E049.
- **E030 drift (reporting-only):** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Golden baseline integrity:** Never let verification overwrite `experiments/*.json`. Restore via `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` if interrupted/dirty.
- **Data coverage:** All `data.download()` inputs must be tracked and pinned in `ledger/data_baseline.json`; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Concrete Next Steps (in order)

1. Confirm `scripts/check.sh` passes clean.
2. If it fails on goldens, restore goldens, then re-run `scripts/check.sh`.
3. **Priority:** Triage E041/E042 numerical stability from ill-conditioned QP (see `ledger/RESEARCH_LEDGER.md` E049). Read `src/portfolio_opt.py` + `tests/test_portfolio_opt.py`, reproduce with `SEED=42 python3 run_all_verification.py --extended`, inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`. Profile the tangency path for conditioning/scaling without changing economic decisions. Any fix must keep constraint validation passing (optimizer validates constraints, not solver exit status).
4. Only after (1)-(3) are stable: consider deferred blend optimization (E015), pre-registered with gates/sensitivity.

## Verification Commands

- Fast integrity: `SEED=42 bash scripts/check.sh`
- Quick verification (restores goldens): `SEED=42 python3 run_all_verification.py`
- Extended (shows E041/E042 drift): `SEED=42 python3 run_all_verification.py --extended`
- Recovery if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Guardrails

- Always use `SEED=42`.
- Never re-pin baselines as a side effect of verification runs.
- Never modify `experiments/*.json` without explicit justification + `scripts/check_golden_baseline.py --update`.
- Pre-register any new experiment before running; no goalpost moving.
- Cost model: tc=0.5bps + slippage=0.2bps, next-day open execution.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

(End of file)
