# HANDOFF_NEXT_SESSION_2026-10-28T11-20-34Z

**Created:** 2026-10-28T11:20:34Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main, up to date with `origin/main`
**HEAD:** 14530eb (chore(kilo): checkpoint agent session)
**Working tree:** clean of tracked changes; only `__pycache__/*.pyc` modified (gitignored — ignore). No `.verify_snapshot/` active; no interrupted verification run.

## Initial Task (do this first)

You are taking over a clean, verified baseline. Do **not** re-run experiments to "update" goldens unless explicitly asked. Follow the guards below.

### 1) Verify baseline integrity (required)
```bash
SEED=42 bash scripts/check.sh
```
Expected: exit 0, "ALL VERIFICATIONS PASSED", "=== All checks passed ===".

**Verified at handoff time:** this command passes. The `FAIL` lines you may see in the raw output are *test fixtures* written by `tests/test_json_guard.py` into a temp dir (e.g. `experiments/d.json`, `experiments/badlist.json`, `experiments/d2.json`) and a stale-snapshot PID marker — they are not real baseline failures. Filter them out; confirm the final `=== All checks passed ===` line and exit code 0.

### 2) Sanity check verification path (recommended)
```bash
SEED=42 python3 run_all_verification.py        # quick (~8 min)
# or
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
```
Do **not** commit any verification output. If interrupted, recover with:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```

### 3) Know the active caveats
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates tangency answers on the problem's constraints, not on the solver's exit status (SLSQP status 8 is acceptable). The tangency QP remains ill-conditioned → E041/E042 grid may show numeric drift (up to ~1e-5). Structural differences must remain zero. Do **not** re-pin to silence numeric drift.
- **E041 open item:** ~133 numeric diffs (1-ulp sensitivity), 3 structural differences already fixed. Do not re-pin; tracked in `ledger/RESEARCH_LEDGER.md` E049.
- **Extended drift reporting:** `--extended` writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). E029 fundamentals and E030 ETF panel are pinned/offline-reproducible; see ledger entries E045/E048.
- **Data coverage enforced:** every `data.download()` call site must have a committed, git-tracked cache file pinned in `ledger/data_baseline.json`. Missing/unpinned inputs fail hard under offline verification (`QUANT_RESEARCH_OFFLINE=1`).
- **Golden discipline:** `experiments/*.json` are canonical. Verification backs up/restores them. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` with explicit intent and a ledger update.

## Read first
- `AGENTS.md` — full commands, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — research state, decisions (REJECTED/PARTIAL), open items
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` — pinned fingerprints
- `scripts/check.sh` — the gate you must satisfy

## Immediate focus
Determine whether there is any open work from the ledger (e.g. the E041 numeric-drift follow-up) or whether you are asked only to run verification/reproduce. If no explicit task is given beyond this handoff, **run (1) above and report status only**. Do not make speculative changes.

**End of handoff.**