# HANDOFF - 2026-10-30T07-25-34Z

## Session Context
- **Repo**: Quantitative-Trading-Public-Research-Prompted (US equities/futures/macro, 2014–2026)
- **Phase**: Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Timestamp**: 2026-10-30T07:25:34Z
- **Objective**: Establish a clean, verified baseline before starting any new work.

## CLEAR INITIAL TASK FOR NEXT AGENTIC SESSION

### Priority 0: Check for stale verification state (BLOCKING)
```bash
ls -la .verify_snapshot/ 2>&1 | head -12
[ -f .verify_snapshot/ACTIVE.json ] && cat .verify_snapshot/ACTIVE.json
```

- If `ACTIVE.json` exists with a live PID → do **NOT** start a new verification run. Recover first.
- If a stale snapshot exists without a live PID → recover before proceeding.
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

### Priority 1: Baseline integrity checks (REQUIRED)
```bash
SEED=42 bash scripts/check.sh
```

This runs: `py_compile`, `check_goldens_clean.py` (working tree vs HEAD), `check_golden_baseline.py` (vs `ledger/golden_baseline.json`), `check_data_coverage.py`, and convention robustness tests. **All must pass.**

### Priority 2: Quick verification (REQUIRED)
```bash
SEED=42 python3 run_all_verification.py
```

Runtime ~8 min. Re-executes the 8 quick drivers + batch/validate + E042 n_sim=2. The suite backs up/restores goldens automatically. **Do not interrupt this run.**

### Priority 3: Report status
After completion, summarize:
- Stale snapshot status and any recovery actions taken
- `scripts/check.sh` result (pass/fail + details)
- Quick verification result (pass/fail)
- Any golden/data mismatches found and how they were resolved
- Anomalies vs known expectations

## Known Expectations
- **E041/E042 numeric drift is expected** due to ill-conditioned tangency QP (optimizer determinism fixed per E049). Focus on structural differences, not 1e-5 numeric noise.
- **E029 and E030 are now offline-reproducible** (pinned fundamentals/panel). They should reproduce with 0 differences.
- **E041** may still show numeric differences (QP sensitivity) — do **not** re-pin to silence them.

## Constraints
- **Never re-pin goldens** as a side effect of verification. Only re-pin via explicit `--update` scripts with justification.
- **Always use SEED=42** for reproducibility.
- **Verification runs in offline mode** (`QUANT_RESEARCH_OFFLINE=1`). Missing cache entries will fail hard.
- **Do not commit verification output**. If interrupted, restore goldens before committing.
- **A verification run must never be left half-finished** (snapshot recovery mechanism is in place).

## Key References
- `AGENTS.md` - Full commands, conventions, and baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` - Experiment history and decisions
- `ledger/golden_baseline.json` - Pinned golden fingerprints
- `ledger/data_baseline.json` - Pinned data fingerprints
- `run_all_verification.py` - Verification orchestrator
- `scripts/check.sh` - Baseline integrity gate

**START HERE. Do not begin new experiments or changes until Priorities 0-2 pass cleanly.**
