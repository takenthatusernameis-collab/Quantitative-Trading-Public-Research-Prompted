# HANDOFF — Quantitative Trading Public Research Prompted
**Timestamp:** 2026-10-31T09:55:06Z
**Branch/Repo:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Current Status
- **Baseline integrity:** Golden artifacts under `experiments/` are pinned. Verification suite backs up/restores them (never modifies canon). Guards in place: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- **Reproducibility:** `SEED=42` required. `run_all_verification.py` supports `--quick`, `--extended`, `--full`, `--skip-slow`, `--restore-only`.
- **Known drift:** E041 has residual numeric drift (133 diffs) due to ill-conditioned QP / 1-ulp sensitivity; structural diffs resolved. Do **not** re-pin to silence. E030/E029 now reproducible offline after pinning inputs.
- **Optimizer:** `src/portfolio_opt.py` validates on constraints (not solver status) per `tests/test_portfolio_opt.py` (fixes env-dependent tangency).
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). Fundamentals pinned for E029. All data coverage enforced.

## Immediate Priorities (for next session)
1. **Verify baseline health** (safe, read-only first)
   ```bash
   SEED=42 bash scripts/check.sh
   # or
   make check
   ```
   If goldens dirty/stale snapshot → run `SEED=42 python3 run_all_verification.py --restore-only`.

2. **Run quick verification** to confirm environment
   ```bash
   SEED=42 python3 run_all_verification.py --quick
   # or make verify-quick
   ```

3. **Address open items from ledger** (if in scope)
   - Review `ledger/RESEARCH_LEDGER.md` for E041/E049 follow-ups (optimizer determinism / acceptable drift policy).
   - Consider E030/E029/E041 drift tolerance policy (numeric-only vs structural). Any change requires re-pinning via explicit scripts, not side effects.
   - CI workflow: `.github/workflow-templates/verification-gate.yml` exists but cannot be auto-created; needs maintainer action.

## Constraints & Rules
- **Never commit verification output.** Restore before committing if interrupted.
- **Pre-registration:** Goalposts never moved post-hoc. Sensitivity grids reported, not gated.
- **Multiple testing:** Promotion needs dedicated pre-registered confirmatory run + full placebo.
- **Determinism:** Use `SEED=42`. Offline mode enforced in verification.
- **Golden policy:** Re-pinning only via `python3 scripts/check_golden_baseline.py --update` with justification; never as side effect of verification.

## Suggested First Task
"Run `SEED=42 bash scripts/check.sh` and report results. If clean, run `SEED=42 python3 run_all_verification.py --quick`. Summarize any failures and propose fixes without re-pinning goldens."

## Key Files
- `AGENTS.md` — full commands/conventions
- `ledger/RESEARCH_LEDGER.md` — research history/open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — fingerprints
- `run_all_verification.py` — orchestration
- `scripts/check.sh` — fast gate
