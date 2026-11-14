# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-14T23:32:46Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` @ `7d0a643c` ("chore(kilo): checkpoint agent session") — in sync with `origin/main`
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Research phase:** complete (E001–E051). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Tracked research/golden artifacts:** clean. `SEED=42 bash scripts/check.sh` exits 0 (all guards pass: goldens clean vs HEAD, golden baseline vs pinned SHA-256, data coverage, experiment-script imports). Verified at handoff time.
- **Verification snapshot:** no active `.verify_snapshot/` present. If a future run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before trusting `experiments/*.json`.
- **Working tree:** clean apart from gitignored `__pycache__/*.pyc` modifications from local checks. No source, experiment, data, ledger, or script changes. Do not commit `__pycache__` noise.
- **Delta vs prior durable handoff** (`handoff_2026-11-14T23:27:39Z_INITIAL_TASK.md`, same HEAD): none material. Prior handoff's active-snapshot/experiments/e001-modified state is gone; working tree is clean and `check.sh` passes. This handoff refreshes the canonical starting point for the next session.

## Initial Task (do first)

1. **Confirm baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0. If it fails with `ModuleNotFoundError`, install dependencies first:
   ```bash
   pip3 install --break-system-packages -r requirements.txt
   ```
   then re-run `check.sh`. Treat dependency/setup failures separately from baseline regressions.

2. **If integrity checks fail for a real reason**
   - Tracked `experiments/*.json` differ from HEAD or pinned baseline: do **not** commit the drift. Recover with `SEED=42 python3 run_all_verification.py --restore-only` or restore the pinned artifact (`git checkout <pinned-commit> -- experiments/<file>` per `ledger/golden_baseline.json`) — not blindly from HEAD if HEAD has been contaminated.
   - Stale/live verification snapshot: recover with `--restore-only`; never start a new verification run while another live snapshot owns `.verify_snapshot/`.
   - Data coverage/fingerprint issue: follow `scripts/check_data_coverage.py` and `AGENTS.md`; never add live-download dependencies or re-pin baselines without explicit justification.

3. **Then idle awaiting explicit user direction**
   - Do **not** make source changes, run long verification suites, or create commits unless explicitly requested.
   - Do **not** modify `experiments/*.json` goldens, `ledger/golden_baseline.json`, or `ledger/data_baseline.json` as a side effect.
   - Do **not** re-pin any baseline to silence drift without explicit instruction and a clear diff rationale.
   - Always use `SEED=42` for verification/reproducibility commands.

## Key Commands

```bash
# Fast integrity gate (~seconds)
SEED=42 bash scripts/check.sh

# Recovery if verification was interrupted
SEED=42 python3 run_all_verification.py --restore-only

# Verification (only when explicitly requested)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)

# Individual guards
python3 scripts/check_goldens_clean.py
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
```

## Known Open Items / Cautions (per AGENTS.md & ledger)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints, not solver exit status. Tangency QP is ill-conditioned; 1-ulp input perturbations can move `min_var` answers (~1e-05), so E041/E042 grid artifacts may show 29–133 numeric diffs in extended runs. **Do not re-pin to silence this.**
- **E041 drift:** remaining numeric sensitivity is open; structural "8 of 96" issue fixed. Do not re-pin `experiments/e041*` artifacts to mask drift.
- **Extended drift reporting:** `--extended` writes gitignored `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` outside `experiments/`; it must not contaminate canonical baselines.
- **Data reproducibility:** cache coverage is enforced (`QUANT_RESEARCH_OFFLINE=1` in suite). Pinned vintages/snapshots are authoritative; commit and re-pin only with explicit intent.
- **CI gate:** `.github/workflows/verification-gate.yml` cannot be created by automated agents here; maintainer must add it via GitHub UI using `.github/workflow-templates/verification-gate.yml`.
- **Baseline discipline:** never commit verification output, never leave a verification run half-finished, never replace golden artifacts without re-pinning and documenting rationale.

## Scope / Next Direction

No new research action is prescribed. Wait for explicit user direction (e.g., targeted bugfix, requested verification run, or a pre-registered new experiment). Any new experiment must follow project pre-registration, falsification, and promotion-gate conventions in `AGENTS.md` and `ledger/RESEARCH_LEDGER.md`.