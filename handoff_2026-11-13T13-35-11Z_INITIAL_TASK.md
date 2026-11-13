# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-13T13:35:11Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `ebe2bc4a994bc15a9a73214948c508c741b2a137` (`chore(kilo): checkpoint agent session`) on `main`, in sync with `origin/main`
**Working tree at handoff:** `M src/__pycache__/cache_keys.cpython-312.pyc` (untracked bytecode only; no tracked changes). `.verify_snapshot/` and `.verify_reports/` absent — no interrupted verification run to recover.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Validated survivors and decisions recorded in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (138 tracked; 107 pinned goldens). Integrity pinned in `ledger/golden_baseline.json` and `ledger/data_baseline.json` (35 pinned data inputs).
- Supersedes prior durable handoff `handoff_2026-11-13T13-34-37Z_INITIAL_TASK.md` (HEAD `a7603f3b`). Delta `a7603f3b..ebe2bc4a` over `experiments/ data/ src/ tests/ scripts/` is **empty** — only `.handoff/*` canonical pointers, `ledger/RESEARCH_LEDGER.md` (the E226 handoff-refresh entry), and `research_state/workflow_run_diagnostics.jsonl` changed. No research/source/data/experiment/baseline substance changed.
- **Baseline guards re-run at this handoff:** `SEED=42 python3 scripts/check_golden_baseline.py` → ALL 107 pinned goldens match (exit 0); `SEED=42 python3 scripts/check_data_coverage.py` → ALL 35 pinned data inputs present, tracked, unchanged (exit 0).

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
   - Proceed with maintenance or new research consistent with the completed phase and project conventions.

## Critical guardrails
- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (no live-network dependence in verification paths).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`).
- **Pre-registration & reporting:** new experiments must pre-register gates/falsification before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — do not re-pin to silence.
- **Do not commit verification output**; restore goldens before committing (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).

## Pending work
- No explicit pending tasks recorded. Confirm baseline health, then await/execute user-directed work consistent with project conventions.
