# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T09:22:49Z
**Session Context:** Research phase complete (E001–E043). Verification infrastructure hardened. Repo working tree clean. Durable handoff for next session.

## Initial Task (Clear & Actionable)

**Focus: Resolve E041 numeric drift (ill-conditioned QP) and harden reproducibility before any new strategy exploration. Do not re-pin baselines.**

## Immediate First Actions

1. `SEED=42 bash scripts/check.sh` — must pass before anything else.
2. If golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only`.
3. Reproduce drift: `SEED=42 python3 run_all_verification.py --extended`; inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`.

## Open Items

- E041 drift: 133 numeric diffs from 1-ulp sensitivity in `src/portfolio_opt.py`. Investigate scaling/ridge without changing economic decisions. See ledger E049.
- Golden baseline integrity: re-pin only with `--update` + justification.
- Data coverage: all `data.download()` inputs tracked in `ledger/data_baseline.json`.

## Guardrails

- Use `SEED=42`. Never re-pin baselines as side effect. Never modify `experiments/*.json` without justification. Offline discipline (`QUANT_RESEARCH_OFFLINE=1`). Pre-register new experiments.

(End of file)
