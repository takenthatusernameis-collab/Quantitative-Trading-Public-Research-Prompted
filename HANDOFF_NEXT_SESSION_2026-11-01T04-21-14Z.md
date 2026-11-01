# Handoff (timestamp: 2026-11-01T04:21:14Z)

## Status
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/HEAD: $(git rev-parse --short HEAD)
- Working tree: clean (no pending changes)

## Project state (from AGENTS.md)
- Research phase complete (E001–E043). Surviving validated strategies in ledger/RESEARCH_LEDGER.md.
- Golden artifacts: experiments/*.json are canonical. Verification backs up/restores (.verify_snapshot/); never leave verification half-finished.
- Pre-registration, multiple-testing discipline, negative results recorded honestly.
- Offline reproducibility enforced for verification (QUANT_RESEARCH_OFFLINE=1) and data coverage pinned (ledger/data_baseline.json).

## Initial task for next session
Start by verifying baseline integrity before any other work: run `SEED=42 bash scripts/check.sh` and confirm `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass. If goldens differ or a snapshot is stale, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) before proceeding. Then read `ledger/RESEARCH_LEDGER.md` for open items (E049 optimizer determinism; E041/E042 QP drift must not be re-pinned to silence). Only perform explicitly requested work; use SEED=42; do not commit verification output or re-pin goldens as a side effect.

## Quick commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow
SEED=42 python3 verify_convention_robustness.py
```

## Notes
- CI workflow cannot be created by agents (controller restores .github/workflows/); template at .github/workflow-templates/verification-gate.yml.
- Data: cached parquet in data/ (gitignored except pinned vintages). Fundamentals pinned for E029.
