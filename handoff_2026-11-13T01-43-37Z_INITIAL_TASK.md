# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-13T01:43:37Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `f3b26965` (`f3b2696562d4467e0381c48c3fba03faab332f4e`, "chore(kilo): checkpoint agent session") on `main`, in sync with `origin/main`.
**Working tree at handoff:** 1 tracked modification — `src/__pycache__/cache_keys.cpython-312.pyc` (stale bytecode build artifact, 3462 bytes, not research substance; never commit). `.verify_snapshot/` absent → no interrupted verification to recover. `.verify_reports/` absent.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Validated survivors and decisions recorded in `ledger/RESEARCH_LEDGER.md` (last research entry E051; E052–E195 are durable-handoff refreshes only).
- Canonical artifacts: `experiments/*.json` — 138 tracked entries (107 pinned goldens + 31 drivers). Integrity pinned in `ledger/golden_baseline.json` and `ledger/data_baseline.json` (35 pinned data inputs).
- Supersedes prior handoff: `handoff_2026-11-13T01-42-12Z_INITIAL_TASK.md` (same repo state; prior handoffs back to `handoff_2026-11-13T00-50-24Z_INITIAL_TASK.md` also superseded).

## Verified at handoff (re-run live)
- `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**
- `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**
- `git diff --name-only 33be527e..f3b26965 -- experiments/ data/ src/ tests/` → **empty** (0 paths). No research, source, data, experiment, or baseline substance changed since the last substantive state.

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
- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (no live-network dependence in verification paths; suite runs with `QUANT_RESEARCH_OFFLINE=1`).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`).
- **Pre-registration & reporting:** new experiments must pre-register gates/falsification before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — do not re-pin to silence.
- **Do not commit** the stale `src/__pycache__/cache_keys.cpython-312.pyc` or any verification output.

## Pending work
- No explicit pending tasks recorded. Confirm baseline health, then await/execute user-directed work consistent with project conventions.