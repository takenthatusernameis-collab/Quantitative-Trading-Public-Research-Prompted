# HANDOFF: Next Agentic Work Session

**Timestamp:** 2026-11-02T15:31:49Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD context:** git repo (see `git log --oneline -5`)
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State (from AGENTS.md)

- **Research phase complete (E001–E043).** Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Verification suite is the source of truth.** `experiments/*.json` are canonical goldens. The suite backs up/restores them; never leave a verification run half-finished.
- **Guards in place:**
  - `scripts/check_goldens_clean.py` fails if tracked `experiments/` differ from HEAD or stale snapshot pending (live runs reported, not failed).
  - `scripts/check_golden_baseline.py` enforces SHA-256 fingerprints in `ledger/golden_baseline.json` (commit-level guard). Re-pin only via `--update`, never as side effect of verification.
  - `scripts/check_data_coverage.py` enforces pinned data coverage (offline verification). Re-pin via `--update` when adding inputs.
- **Known open/delicate items:**
  - **E041 drift (open):** Optimizer determinism issue fixed (SLSQP status 8 no longer gated), but ill-conditioned QP leaves ~133 numeric diffs vs 1e-4 tolerance; structural diffs gone. Do **not** re-pin to silence.
  - **E030:** Now reproducible with pinned panel (was network/yfinance dependent).
  - **E029:** Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline reproducible).
  - **Optimizer determinism:** Validated on problem constraints (see `tests/test_portfolio_opt.py`). Ill-conditioning remains.
- **CI:** Verification gate workflow cannot be created by agents (controller restores `.github/workflows/`). Template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.

## Immediate Goal for Next Session

**Verify repo integrity and establish a clean baseline before any new work.** Do not modify `experiments/` goldens or `ledger/*_baseline.json` unless there is a documented, intentional re-pin with justification.

## Suggested First Steps (in order)

1. **Check for stale verification state**
   - Look for `.verify_snapshot/ACTIVE.json` and any uncommitted changes to `experiments/`.
   - If stale snapshot exists or working tree dirty with experiment changes from interrupted run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` as appropriate).

2. **Run fast integrity checks**
   - `SEED=42 bash scripts/check.sh` (convention robustness + template validation + guards)
   - Pay attention to: `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `tests/test_portfolio_opt.py`.

3. **Quick reproducibility sanity (optional but recommended)**
   - `SEED=42 python3 run_all_verification.py --skip-slow` (faster) or `make verify-quick` if time allows.
   - Compare against expectations in AGENTS.md (extended drift report may appear in `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` if running extended).

4. **Review ledger for context**
   - Read `ledger/RESEARCH_LEDGER.md` (E041/E048/E049 especially) to understand open items and constraints.

## Constraints / Rules to Follow

- **Seed:** always `SEED=42`
- **Never re-pin baselines** as side effect of verification. Use `--update` only with explicit justification and document in commit message.
- **Offline verification:** suite runs with `QUANT_RESEARCH_OFFLINE=1`; missing pinned data must fail.
- **Convention:** close-to-close v1.2.3 primary; overnight decomposition reported.
- **No new goldens from interrupted runs:** restore first if in doubt.
- **Lint:** `python3 -m py_compile` on changed files (no separate linter configured).

## Open Questions / Next Decisions

- [ ] Is `.verify_snapshot/` clean (no ACTIVE.json)?
- [ ] Do `check.sh` and guards all pass?
- [ ] Should we investigate E041 further or leave as documented open item?
- [ ] Any new experiment work requested? If not, focus on integrity/CI template only.

**Initial task for next session:** "Run integrity checks (check.sh), ensure no stale verification snapshot, restore goldens if needed, and report status. Do not modify baselines or experiments."
