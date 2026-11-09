# Handoff — 2026-11-09T14:27:36Z (Initial Task for Next Session)

## Session Context
- **Project**: Quantitative-Trading-Public-Research-Prompted
- **Repo**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Branch**: `main` (HEAD: `b219a7c3`, recent checkpoint commits)
- **Phase**: Research complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Baseline state at handoff**: Working tree clean; committed golden artifacts match HEAD (`scripts/check_goldens_clean.py`).

## Key Commands
```bash
# Baseline integrity / fast check (~seconds)
SEED=42 bash scripts/check.sh
# or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or: make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# or: make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
# or: make verify-full

# Convention robustness only
SEED=42 python3 verify_convention_robustness.py
# or: make verify

# Recovery if verification is interrupted
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```

## Critical Invariants (read before changing anything)
1. **`experiments/*.json` are canonical goldens.** Verification overwrites and restores them; never leave a run half-finished. A golden mismatch vs HEAD must be fixed before committing.
2. **Golden baseline fingerprints**: `ledger/golden_baseline.json` pins SHA-256s. Replacing an artifact requires explicit `python3 scripts/check_golden_baseline.py --update` — never as a side effect of verification.
3. **Data caches are pinned and enforced.** Vintages in `data/vintages.json` / `data/fundamentals_vintages.json`; cache coverage checked by `scripts/check_data_coverage.py`. Verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
4. **Reproducibility**: Always `SEED=42`. Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
5. **Pre-registration discipline**: New experiments need pre-registered gates/falsification/sensitivity grid; grid results are reported, not gated. Negative results recorded honestly (REJECTED/PARTIAL). Do not move goalposts post-hoc.

## Open Items (do not “fix” by re-pinning without evidence)
- **E041 optimizer drift** (133 numeric diffs in extended verification; 3 structural diffs resolved per E049). Ill-conditioned QP / 1-ulp sensitivity remains; do **not** re-pin E041/E042 grid artifacts to silence drift.
- **E042 grid artifacts** may show bounded numeric drift for the same reason.
- **CI gate**: Template at `.github/workflow-templates/verification-gate.yml` — must be created manually via GitHub UI (agents lack workflow push permission).

## Suggested First Actions for Next Session
1. Run `SEED=42 bash scripts/check.sh` to confirm baseline integrity.
2. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies, dispositions, and open items.
3. If making changes, identify whether they affect goldens/data baselines; follow the explicit update/pin procedures above.
4. If running verification, let it complete; use `--restore-only` on interruption before any commit.
