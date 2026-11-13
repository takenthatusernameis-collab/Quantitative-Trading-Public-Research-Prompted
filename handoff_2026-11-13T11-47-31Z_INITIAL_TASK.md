# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-13T11:47:31Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `252a2ab8` on `main`, working tree clean (no tracked/untracked changes). `.verify_snapshot/` and `.verify_reports/` absent.
**Supersedes:** `handoff_2026-11-13T09-45-00Z_INITIAL_TASK.md` (HEAD `a913b01b`).

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Validated survivors/decisions recorded in `ledger/RESEARCH_LEDGER.md` (E051 last research entry; subsequent E052+ entries are durable-handoff/housekeeping refreshes).
- Canonical artifacts: `experiments/*.json` (138 tracked; 107 pinned goldens). Integrity baselines: `ledger/golden_baseline.json`, `ledger/data_baseline.json`.

## Initial task for the next session
1. **Establish baseline integrity before any changes**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Confirm golden cleanliness/baselines, data coverage, compile/tests, and conventions. Do not commit if mismatches are reported.
2. **If verification/reproduction is requested**, run the appropriate suite (per `AGENTS.md`):
   - Quick: `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
   - Extended/full: `--extended` / `--full` as needed
   Suites overwrite and restore `experiments/*.json`; never leave a run half-finished. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
3. **Review context, then take only user-directed work**
   - Read: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent durable handoffs.
   - Proceed with maintenance or new research consistent with the completed phase and project conventions.

## Critical guardrails
- **Reproducibility:** always `SEED=42`; rely on pinned data vintages/caches (no live-network dependence in verification paths).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`).
- **Pre-registration & reporting:** new experiments must pre-register gates/falsification before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL). Do not move goalposts post-hoc.
- **Known drift (do not "fix" by re-pinning):** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (ledger E049/open item); extended verification may report E041 numeric drift within that context.

## Pending work
- No explicit pending research tasks recorded. Confirm baseline health, then await/execute user-directed work consistent with project conventions.