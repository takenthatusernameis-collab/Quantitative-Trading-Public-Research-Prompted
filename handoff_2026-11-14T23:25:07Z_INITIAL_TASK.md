# Initial Task — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T23:25:07Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Phase:** Research complete (E001–E043). Validated survivors documented in `ledger/RESEARCH_LEDGER.md`.
**Working dir:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Start Here (integrity-first)

1. **Check baseline/worktree integrity (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```
   - Fails if `experiments/*.json` differ from HEAD or from `ledger/golden_baseline.json`, if `.verify_snapshot/ACTIVE.json` is stale/live, or if pinned data coverage is missing. Do not commit verification output.

2. **If a previous verification run was interrupted, restore goldens first:**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   # fallback (only if HEAD is the true pinned baseline): git checkout -- experiments/
   ```

3. **Run verification as needed:**
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
   - Extended (~21 min, 8 quick + 18 drivers, structural match): `SEED=42 python3 run_all_verification.py --extended` / `make verify-extended`
   - Full (~15 min, E042 n_sim=50 + 96-config grid): `SEED=42 python3 run_all_verification.py --full` / `make verify-full`
   - Convention-only: `SEED=42 python3 verify_convention_robustness.py` / `make verify`

## Known State / Constraints (do not "fix" by re-pinning)

- **Canonical artifacts:** `experiments/*.json` are golden baselines; suite overwrites then restores. Never re-pin goldens as a side effect of verification (`ledger/golden_baseline.json` requires explicit `--update`).
- **Seed:** always `SEED=42`. Data/fundamentals vintages and cache coverage are enforced (`ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, `scripts/check_data_coverage.py`). Runs use offline mode where applicable.
- **Extended drift (expected, reporting):** 15/18 drivers 0-diff; **E041** has ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP, optimizer determinism fixed per ledger E049, decision REJECTED 3/5 unchanged) — still exceeds 1e-4 tolerance, **do not re-pin**. E029/E030 offline-reproducible with pinned snapshots. See `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) after `--extended`.
- **Working tree note at handoff creation:** modified `__pycache__/*.pyc` files present (`scripts/`, `src/`, `tests/`); no `experiments/` diffs observed. Treat pyc churn as non-canonical noise unless policy states otherwise.

## Suggested Initial Task for This Session

1. Run `SEED=42 bash scripts/check.sh` and report pass/fail with any integrity issues.
2. If clean, run `SEED=42 python3 run_all_verification.py --extended` to refresh the drift report; summarize results vs known expectations (especially E041) without modifying goldens/baselines.
3. Consult `ledger/RESEARCH_LEDGER.md` for open items (e.g. E041/E042 QP conditioning) and propose/execute only pre-registered, evidence-backed follow-ups if requested; record negative results honestly.
4. Leave an updated timestamped handoff if material state changes.

## References

- `AGENTS.md` — commands, baseline-integrity rules, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — experiment outcomes and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
