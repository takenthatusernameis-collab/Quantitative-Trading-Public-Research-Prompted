# HANDOFF_NEXT_SESSION_2026-10-28T11-24-40Z

**Created:** 2026-10-28T11:24:40Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main, up to date with `origin/main`
**HEAD:** 14530eb (chore(kilo): checkpoint agent session)
**Working tree:** clean of tracked changes; only `__pycache__/*.pyc` modified (gitignored — ignore). No `.verify_snapshot/` active; no interrupted verification run.

## Clear initial task for next session

Start here in order:

1. **Verify baseline integrity (required)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expected: exit 0, "ALL VERIFICATIONS PASSED", "=== All checks passed ===". Filter out test-fixture `FAIL` lines from `tests/test_json_guard.py` (e.g. `experiments/d.json`, `experiments/badlist.json`, `experiments/d2.json`) and the stale-snapshot PID marker — they are not real baseline failures.

2. **Read the ledger**
   - Read `ledger/RESEARCH_LEDGER.md` top-to-bottom. Pay special attention to E041/E042 and the "do not re-pin" policy.

3. **Confirm reproducibility state (recommended)**
   ```bash
   SEED=42 python3 run_all_verification.py        # quick (~8 min)
   ```
   Do not commit verification output; recover interrupted runs with `--restore-only`.

4. **Decide next action**
   - Follow the ledger's stated disposition. If an explicit open item exists (e.g. E041 numeric-drift follow-up), tackle it; otherwise run (1) and report status only. Do not make speculative changes; do not re-pin baselines to silence drift.

## Key caveats
- Optimizer determinism (E049): `src/portfolio_opt.py` validates on problem constraints, not solver status. Ill-conditioned QPs may show numeric drift (up to ~1e-5); structural differences must remain zero. Do not re-pin.
- E041: ~133 numeric diffs, 3 structural differences already fixed. Do not re-pin.
- Data coverage enforced: every `data.download()` call site must have a committed, git-tracked cache file pinned in `ledger/data_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Golden discipline: `experiments/*.json` are canonical. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` with explicit intent and a ledger update.

## Read first
- `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `scripts/check.sh`

**End of handoff.**
" filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/HANDOFF_NEXT_SESSION_2026-10-28T11-24-40Z.md"