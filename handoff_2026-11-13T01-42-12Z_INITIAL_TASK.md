# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-13T01:42:12Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `dd6dedf9` (on `main`, in sync with `origin/main`)
**Working tree at handoff:** clean (one untracked pyc file). `.verify_snapshot/` absent.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Validated survivors and decisions recorded in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (pinned goldens + drivers). Integrity pinned in `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- Supersedes prior handoff: `handoff_2026-11-13T01-41-50Z_INITIAL_TASK.md` (same repo state).

## Initial task for the next session
1. **Establish baseline integrity before any changes**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Confirms golden cleanliness/baselines, data coverage, compile/tests, and conventions. Do not commit if mismatches are reported.
2. **If verification/reproduction is requested**, run the appropriate suite (see `AGENTS.md`):
   - Quick: `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
   - Extended/full as needed (`--extended`, `--full`)
   Suites overwrite and restore `experiments/*.json`; never leave a run half-finished. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
3. **Review context, then take only user-directed work**
   - Read: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent durable handoffs.
   - Proceed with maintenance or new research consistent with completed phase and project conventions.

## Critical guardrails
- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (no live-network dependence in verification paths).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`).
- **Pre-registration & reporting:** new experiments must pre-register gates/falsification before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — do not re-pin to silence.

## Pending work
- No explicit pending tasks recorded. Confirm baseline health, then await/execute user-directed work consistent with project conventions.
