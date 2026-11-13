# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-13T14:34:32Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `168c1071` (`chore(kilo): checkpoint agent session`) on `main` (in sync with `origin/main` per prior state; re-check with `git status -sb` / `git rev-list --left-right --count origin/main...HEAD`).
**Working tree at handoff:** only tracked `__pycache__/*.pyc` bytecode files modified (from routine interpreter runs / dependency installs). **No source, data, experiment, ledger, or baseline changes.** `.verify_snapshot/` and `.verify_reports/` absent.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. **Research phase complete (E001–E043).**
- Canonical artifacts: `experiments/*.json` (tracked goldens pinned in `ledger/golden_baseline.json`) and pinned data inputs in `ledger/data_baseline.json`. Decisions and survivor status recorded in `ledger/RESEARCH_LEDGER.md`.
- Recent commits since the 14:33:02Z handoff are checkpoint-only/session bookkeeping; no research/source/data/experiment/baseline substance changed. Prior durable handoff: `handoff_2026-11-13T14-33-02Z_INITIAL_TASK.md`.
- **Do not commit `__pycache__/` changes** — treat as local noise.

## Initial task for the next session
1. **Establish a clean, healthy baseline before any changes**
   ```bash
   pip install -r requirements.txt        # if dependencies are missing
   SEED=42 bash scripts/check.sh          # goldens/baselines, data coverage, compile/tests, conventions
   ```
   Do not proceed with commits if mismatches are reported. If a stale/interrupted verification snapshot is reported, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
2. **If verification or reproduction is requested**, run the appropriate suite (see `AGENTS.md`): `make verify-quick` / `SEED=42 python3 run_all_verification.py`, or `--extended` / `--full` as needed. Suites overwrite and restore `experiments/*.json` — never leave a run half-finished.
3. **Review context, then perform only user-directed work**
   - Read: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent durable handoffs (e.g. this file / `handoff_NEXT_SESSION_INITIAL_TASK.md`).
   - Proceed with maintenance or new research consistent with the completed phase and project conventions.

## Critical guardrails
- **Reproducibility:** always `SEED=42`; rely on pinned data vintages/caches (no live-network dependence in verification paths).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`).
- **Pre-registration & reporting:** pre-register gates/falsification before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — do not re-pin to silence.
- **Verification output:** do not commit verification output; restore goldens before committing (`--restore-only` or `git checkout -- experiments/` when appropriate for pinned baseline).

## Pending work
- No explicit pending tasks recorded. Confirm baseline health, then await and execute user-directed work consistent with project conventions.
