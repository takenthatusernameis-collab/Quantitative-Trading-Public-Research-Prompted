# HANDOFF — Timestamped Initial Task for Next Agentic Session

**Timestamp (UTC):** 2026-11-02T07:02:52Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Head commit:** c89a00d (chore(kilo): checkpoint agent session)
**Working tree:** modified __pycache__ files (see git status) — uncommitted bytecode changes; do not commit unless intentional

## What was just done (context)
- Latest checkpoint commit recorded session state.
- Working tree has modified `.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`. These are likely from previous test runs/verification; they are not source changes. Consider `git clean -fdx` only if you need a pristine build environment, but be careful not to delete local data artifacts.

## Current state (from AGENTS.md)
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure hardened (snapshot backup/recovery, golden baseline guard, data coverage guard, optimizer determinism fix noted).
- Key commands: `make check` (fast), `make verify-quick` (~8 min), `make verify-extended` (~21 min), `make verify-full` (~15 min). Use `SEED=42`.
- Baseline integrity: never leave verification half-finished; use `SEED=42 python3 run_all_verification.py --restore-only` if interrupted. `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` enforce guards.
- E029/E030 now offline-reproducible via pinned data; E041 has optimizer-determinism related drift noted (open item).

## Clear initial task for next agent
**Priority 1: Establish a clean, verifiable baseline before making changes**
1. **Verify environment**: Run `SEED=42 bash scripts/check.sh` and ensure it passes (or report failures clearly). This runs py_compile, guards (goldens clean, golden baseline, data coverage, JSON artifacts), and convention robustness.
2. **Understand guards**: Read `ledger/golden_baseline.json` and `ledger/data_baseline.json` to know pinned fingerprints.
3. **Check for stale snapshot**: Ensure no stale `.verify_snapshot/ACTIVE.json` exists. If present and process not running, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

**Priority 2: Orient to current research state**
1. **Read ledger**: Skim `ledger/RESEARCH_LEDGER.md` (especially latest entries E045–E049) to understand open items and dispositions.
2. **Identify next work**: Check if there are any TODOs/FIXMEs related to open items (E041 drift, etc.) or follow-up experiments. If unclear, propose a plan and confirm before implementing.

**Priority 3: Make changes safely**
1. **Follow conventions**: Pre-register changes, respect multiple-testing discipline, never move goalposts post-hoc.
2. **Preserve baselines**: Do not re-pin goldens/data unless explicitly justified and recorded. Use guards.
3. **Test**: Run relevant tests (`pytest` or suite) and `scripts/check.sh` before committing.

## Notes / gotchas
- `pyc` files modified — can ignore or clean.
- Verification can overwrite `experiments/*.json` temporarily; guards prevent silent baseline replacement.
- `cvxpy` optional; optimizer falls back to scipy.
- Offline mode enforced in verification (`QUANT_RESEARCH_OFFLINE=1`).

## Suggested first command
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
SEED=42 bash scripts/check.sh
```
