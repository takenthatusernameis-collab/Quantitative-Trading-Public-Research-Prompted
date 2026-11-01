# HANDOFF: Next Agentic Work Session

**Timestamp (UTC):** 2026-11-01T16:16:05Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Initial Task (Start Here)

1. **Verify baseline integrity (required before any changes)**
   - [ ] Check for stale verification snapshots: `ls -la .verify_snapshot/` (should be absent or have no `ACTIVE.json` from a dead run). If present and stale, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
   - [ ] Run convention + golden integrity checks: `SEED=42 bash scripts/check.sh` (runs py_compile, tests including `tests/test_portfolio_opt.py`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, convention robustness).
   - [ ] Confirm `git status` is clean with respect to `experiments/*.json` (goldens must match `HEAD` and `ledger/golden_baseline.json`).

2. **Get oriented**
   - [ ] Read `ledger/RESEARCH_LEDGER.md` (focus on open items: E041 numeric drift/optimizer determinism; E029/E030/E048/E049 context).
   - [ ] Review `AGENTS.md` "Baseline Integrity" and "Reproducibility" sections (critical guardrails).
   - [ ] Skim recent commits if needed (`git log --oneline -5`).

3. **Decide next action based on user request**
   - If user gives a specific task: do only that, respecting guardrails below.
   - If no specific task: do **not** re-run the full verification suite. Only run targeted checks if investigating a known issue.

## Known Open Items (Do Not Ignore)

- **E041 drift (open):** Extended verification still reports E041 drifting (133 numeric diffs). Optimizer determinism fixed (SLSQP status 8 acceptable if feasible/optimal per `tests/test_portfolio_opt.py`), but ill-conditioned tangency QP causes 1-ulp sensitivity. **Do not re-pin `experiments/e041*.json` to silence this.**
- **Data coverage enforced:** `scripts/check_data_coverage.py` requires every `data.download()` cache file to exist, be git-tracked, and match `ledger/data_baseline.json`. Missing/unpinned inputs will fail hard under offline verification.
- **Verification safety:** `run_all_verification.py` backs up/restores `experiments/`. Never leave a run half-finished. Extended reports go to `.verify_reports/` (gitignored).

## Guardrails

- **Seeds:** Always use `SEED=42`.
- **Goldens:** `experiments/*.json` are canonical. Never modify them as a side effect of verification. If a checkpoint commit accidentally replaced them, restore from the correct pinned commit per `ledger/golden_baseline.json` (see AGENTS.md).
- **Re-pinning:** Only re-pin baselines/data via the explicit `--update` flags on the check scripts with justification. Do not do it automatically.
- **Offline:** Verification uses `QUANT_RESEARCH_OFFLINE=1`. If re-running drivers manually, consider setting it to avoid network downloads.
- **CI workflows:** Cannot create/commit `.github/workflows/` (controller restores). Use `.github/workflow-templates/verification-gate.yml` if needed.
- **Commits:** Only commit when explicitly requested by the user.

## Quick Commands

```bash
# Integrity
SEED=42 bash scripts/check.sh

# Quick sanity (8 drivers + batch/validate)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```
