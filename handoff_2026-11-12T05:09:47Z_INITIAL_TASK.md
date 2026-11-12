# Agentic Handoff — Initial Task Message

**Created:** 2026-11-12T05:09:47Z (UTC)
**Session:** New agentic work session — durable handoff
**Status:** Initial — no work completed in this session.

## Repository state

- Quantitative trading research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043); validated strategies in `ledger/RESEARCH_LEDGER.md`.
- `HEAD`: `3016719d` `chore(kilo): checkpoint agent session` (branch `main` in sync with `origin/main` at handoff).
- Canonical artifacts: `experiments/*.json` are committed goldens (tracked). Verification backs them up and restores them — never commit verification output.
- Working tree: only `__pycache__/*.pyc` timestamp drift (untracked/ignored build artifacts in effect); no golden, source, or ledger changes.
- `.verify_snapshot/` absent (no interrupted verification run pending).

## Initial task for next session

1. **Establish a clean, verified baseline before any edits (offline, seconds):**
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```
   Runs `py_compile`, `check_goldens_clean.py`, `check_golden_baseline.py` (SHA-256 vs `ledger/golden_baseline.json`), `check_data_coverage.py`, and `tests/test_portfolio_opt.py`. Writes nothing to `experiments/`.
   - **Success:** exits 0 with no golden mismatch, no stale/pending snapshot, no coverage failure, and tests pass.
   - **If it fails:** fix before committing. Do not capture verification output into `experiments/`. For interrupted runs recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only if `HEAD` holds the pinned baseline).

2. **Report baseline status clearly** (pass/fail and any failures). Do not start feature/research work until baseline is clean.

3. **Only if explicitly requested after a green baseline:** proceed with the requested task following repo conventions (pre-registration, `SEED=42`, `QUANT_RESEARCH_OFFLINE=1` in suite, no goalpost changes, no silent re-pinning).

## Known open items (do not paper over)

- **E041:** 133 numeric diffs remain from 1-ulp QP sensitivity (ledger E049); extended verification still reports drift. Do **not** re-pin `experiments/e041*.json`.
- **E042:** min-var confirmatory **PARTIAL** (4/5; G2 β-constrained placebo z 2.11 < 3.0 FAIL). Market-neutral-total-portfolio line **CLOSED/not promoted**.
- **Process:** never re-pin golden/data baselines as a side effect of verification. Golden re-pin requires `python3 scripts/check_golden_baseline.py --update`; data input requires commit + `python3 scripts/check_data_coverage.py --update` (both reviewed).

## Conventions / reminders

- Reproducibility: `SEED=42`. Quick verify: `make verify-quick`; extended: `make verify-extended`; full: `make verify-full`.
- Drivers run offline under verification (`QUANT_RESEARCH_OFFLINE=1`); cache coverage pinned in `ledger/data_baseline.json`.
- No separate linter; `python3 -m py_compile` on changed Python. No comments/emojis unless requested. Do not commit secrets. Do not commit or push unless explicitly asked.
